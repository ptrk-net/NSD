# Import python libraries
import logging
import numpy as np
import os.path
from joblib import dump, load
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier

# Import local libraries
from bin.NSD_Database import NSD_Database
from bin.NSD_Packets_Queue import NSD_Packets_Queue
from bin.NSD_Monitor import NSD_Monitor_Data
from conf import variables as vrb
from conf import settings as cfg


class NSD_ML:

  def __init__(self, log_level, sync_queue, db_name, daemon, training):
    self.log_level = log_level
    self.logger = logging.getLogger(__name__)
    self.SQ = sync_queue
    self.db_server = cfg.DB_SERVER
    self.db_port = cfg.DB_PORT
    self.db_name = db_name
    self.daemon = daemon

    if os.path.exists(cfg.CLF_MCC) and os.path.exists(cfg.CLF):
      self.MCC = load(cfg.CLF_MCC)
      self.CLF = load(cfg.CLF)
      if self.log_level >= vrb.INFO_ML:
        self.logger.info('Classifier loaded.')
    else:
      self.logger.error('Files \'{}\' or \'{}\' do not exist.'.format(cfg.CLF, cfg.CLF_MCC))
      self.SQ.put('KILL')

  def fork_database(self):
    self.DB = NSD_Database(self.log_level, self.db_server, self.db_port, self.db_name, self.SQ)

  def get_flows(self, prot):
    flows_returned = []
    while True:
      for flow in getattr(NSD_Monitor_Data(), 'get_flows_' + prot)():
        if flow not in flows_returned:
          flows_returned.append(flow)
          yield flow

  def get_counter_PDU(self, pkts):
    counters_PDU = list()
    last_type = 0
    counter = 0
    for pkt in pkts:
      rtp_type = int.from_bytes(pkt['Data'][1:2], byteorder='big')
      if rtp_type == 124 or rtp_type == 103:
        if rtp_type == last_type:
          counter += 1
        else:
          last_type = rtp_type
          # To discard the first two group of PDU of any conversation
          if counter >= 20:
            counter = 0
          elif counter == 0:
            counter += 1
          else:
            counter = 0
            counters_PDU.append(counter)

    return counters_PDU

  def get_features(self, dataset, T, S, features):
    diffs = list()
    dset_features = list()
    block = [0, dataset[0], dataset[1]]
    dataset = dataset[2:]
    count_groups = 0

    x = range(-S, S + 1)
    A = np.array(np.meshgrid(x, x, indexing='xy')).T.reshape(-1, S).tolist()
    A_counter = [0] * len(A)

    for count_PDU in dataset:
      block.pop(0)
      block.append(count_PDU)
      b = 1
      while b < T:
        diff = block[0] - block[b]
        diff = diff > S and S or (diff < -S and -S or diff)
        diffs.append(diff)
        b += 1
      i = A.index(diffs)
      A_counter[i] += 1
      count_groups += 1
      if count_groups == features:
        dset_features.append(A_counter[:])
        A_counter = [0] * len(A)
        count_groups = 0
      diffs.clear()
    return dset_features

  def RTP_get_training_datasets(self):
    dataset_CC = []
    dataset_NCC = []
    counter_flows = 0
    still_flows = True

    flows = self.get_flows('RTP')
    while still_flows:
      flow = next(flows)
      counter_flows += 1
      pkts = self.DB.get_RTP_traffic_by_id(flow[0])
      if self.log_level >= vrb.INFO_ML:
        self.logger.info('Get Training Dataset: {} -> {}'.format(flow[0], int(flow[2])))
      if int(flow[2]) == 1:
        dataset_CC.extend(self.get_counter_PDU(pkts))
      else:
        dataset_NCC.extend(self.get_counter_PDU(pkts))

      if self.log_level >= vrb.DEBUG:
        self.logger.debug('counter {} | flows {}'.format(counter_flows,
                                                         NSD_Monitor_Data.get_total_flows_RTP()))
      if counter_flows == NSD_Monitor_Data.get_total_flows_RTP():
        still_flows = False

    total_len = min(len(dataset_NCC), len(dataset_CC))
    return dataset_NCC[:total_len], dataset_CC[:total_len]

  def get_RTP_features(self, features, T, S):
    counter_flows = 0

    self.fork_database()

    flows = self.get_flows('RTP')
    while True:
      flow = next(flows)
      self.logger.info('Getting features for flow \'{}\'..'.format(flow[0]))

      counter_flows += 1
      pkts = self.DB.get_RTP_traffic_by_id(flow[0])
      groups_PDU = self.get_counter_PDU(pkts)
      if len(groups_PDU) < (features + T):
        groups_PDU.clear()
        self.logger.error('NSD_Flow \'{}\' does not have enough traffic.'.format(flow[0]))
        if not self.daemon:
          self.SQ.put('KILL')
      else:
        feat = self.get_features(groups_PDU, T, S, features)
        NSD_Packets_Queue.insert_RTP_Group_Features([flow[0], feat])
        self.logger.info('Got features for flow \'{}\''.format(flow[0]))

  def evaluate(self, pcap):
    sum_prediction = 0

    self.fork_database()

    while True:
      if self.log_level >= vrb.INFO:
        self.logger.info('Evaluate: getting data set...')
      flow_info = NSD_Packets_Queue.get_RTP_PDU_Groups()

      self.logger.info('Evaluate: predicting for id \'{}\'..'.format(flow_info[0]))
      for feat in flow_info[1]:
        sum_prediction += int(self.CLF.predict(np.array(feat).reshape(1, -1)))

      flow_status = NSD_Monitor_Data.get_status_flow_RTP(flow_info[0])
      if sum_prediction == 0 and self.log_level == vrb.DEBUG:
        if flow_status[0] == vrb.FLOW_FINISHED:
          self.logger.info(
            'NSD_Flow \'{}\' does not seem to have a network covert channel!'.format(flow_info[0]))
          NSD_Monitor_Data.update_status_flow_RTP(flow_info[0],
                                                  [flow_status[0], vrb.FLOW_ML_FINISHED, vrb.FLOW_ML_NEGATIVE])
        else:
          self.logger.info(
            'NSD_Flow \'{}\' does not seem to have a network covert channel... by now'.format(flow_info[0]))
      else:
        IP = self.DB.get_RTP_identification_by_id(flow_info[0])
        self.logger.critical(
          'NETWORK COVERT CHANNEL! With {} MCC metric, Source IP {} and Destination IP {}, RTP'.format(
            self.MCC, IP[0], IP[1]
          ))
        NSD_Monitor_Data.update_status_flow_RTP(flow_info[0],
                                                [flow_status[0], vrb.FLOW_ML_FINISHED, vrb.FLOW_ML_POSITIVE])
        sum_prediction = 0

      if pcap:
        if self.log_level >= vrb.INFO_ML:
          self.logger.info('Dropping temporal database..')
        self.DB.drop_database()
        self.SQ.put('KILL')

  def training(self, features, T, S):
    self.fork_database()

    self.logger.info('Training: getting data sets..')
    dataset_NCC, dataset_CC = self.RTP_get_training_datasets()

    self.logger.info('Training: getting features..')
    feat_NCC = self.get_features(dataset_NCC, T, S, features)
    feat_CC = self.get_features(dataset_CC, T, S, features)

    sum_feat = len(feat_NCC)
    X_train, X_test, y_train, y_test = train_test_split(np.concatenate([feat_NCC, feat_CC]),
                                                        np.concatenate([np.zeros(sum_feat), np.ones(sum_feat)]),
                                                        test_size=0.2, shuffle=True)

    for i in range(0, cfg.TRAINING_ITERATIONS):
      self.logger.info('NSD_Init iteration number {}'.format(i))

      clf = AdaBoostClassifier(base_estimator=RandomForestClassifier(max_depth=10),
                               n_estimators=10000,
                               learning_rate=0.1)
      clf.fit(X_train, y_train)
      predicted = clf.predict(X_test)
      mcc = metrics.matthews_corrcoef(y_test, predicted)
      if mcc > self.MCC:
        self.logger.info('Classifier improved! New MCC metric value: {}'.format(mcc))
        dump(clf, cfg.CLF)
        dump(mcc, cfg.CLF_MCC)
        self.logger.info('New classifier saved.')

    self.SQ.put('KILL')
