# Import python libraries
import logging
from datetime import datetime
import time
import numpy as np
#import matplotlib.pyplot as plt
#from scipy.stats import gaussian_kde
from sklearn import datasets, svm, metrics
from sklearn.model_selection import train_test_split


# Import NSD libraries
from bin.NSD_Database import NSD_Database
from bin.NSD_Monitor_Data import NSD_Monitor_Data
from conf import variables as opts


class NSD_AI:

    def __init__(self, log_level, db_server, db_port, sync_queue):
        self.log_level = log_level
        self.logger = logging.getLogger(__name__)
        self.SQ = sync_queue
        self.db_server = db_server
        self.db_port = db_port

    def NSD_Flow_fork_database(self):
        self.DB = NSD_Database(self.log_level, self.db_server, self.db_port, self.SQ)  # MongoDB


    def NSD_AI_training_get_set(self, type_cc, prot, chats, packets, bbdd):
        # First, wait until there are flows to analyze
        flows = []
        while not flows and not bbdd:
            time.sleep(5)
            #self.logger.info(' - flows: ' + str(flows))
            flows = getattr(NSD_Monitor_Data(), 'NSD_Monitor_Data_get_flows_' + prot + bbdd)()

        if not flows and bbdd:
            flows = [['aaaaaaa']]

        # Then, create the data training set
        data_training_set = []
        data_chat = []
        counter_chats = 0
        counter_packets = 0
        counter_diffs_out = 0
        intervals = [64.0, 67.31333333, 70.62666667, 73.94, 77.25333333, 80.56666667, 83.88, 87.19333333, 90.50666667,
                     93.82, 97.13333333, 100.44666667, 103.76, 107.07333333,110.38666667, 113.7, 117.01333333,
                     120.32666667, 123.64, 126.95333333, 130.26666667, 133.58, 136.89333333, 140.20666667, 143.52,
                     146.83333333, 150.14666667, 153.46, 156.77333333, 160.08666667, 163.4]
        for flow in flows:
            pkts_date = getattr(self.DB, 'NSD_Database_get_' + prot + bbdd + '_date_by_id')(flow[0])
            if type_cc == opts.CC_PT1:
                pkt_date_before = datetime.strptime(pkts_date.pop(0)['Date'], '%d/%m/%Y %H:%M:%S.%f')
                for pkt_date in pkts_date:
                    pkt_date_next = datetime.strptime(pkt_date['Date'], '%d/%m/%Y %H:%M:%S.%f')
                    diff = (pkt_date_next - pkt_date_before).total_seconds()*100000
                    if diff < 250:
                        data_chat.append(diff)
                        counter_packets += 1
                        if counter_packets == packets:
                            (hist, bin_edges) = np.histogram(data_chat, bins=intervals)
                            data_training_set.append(hist)
                            counter_packets = 0
                            data_chat.clear()
                            counter_chats += 1
                            if counter_chats == chats:
                                return data_training_set, intervals
                    else:
                        counter_diffs_out += 1
                    pkt_date_before = pkt_date_next

    # PT1 training
    def NSD_AI_training_PT1(self, chats, data_ts_Not_CC, data_ts_CC):
        classifier = svm.SVC(gamma=0.001)
        X_train, X_test, y_train, y_test = train_test_split(np.concatenate([data_ts_Not_CC, data_ts_CC]),
                                                            np.concatenate([np.zeros(chats), np.ones(chats)]),
                                                            test_size=0.1, shuffle=False)
        classifier.fit(X_train, y_train)
        predicted = classifier.predict(X_test)
        print("Classification report for classifier %s:\n%s\n"
              % (classifier, metrics.classification_report(y_test, predicted)))


        """
        datediff = []
        pkts_date = self.DB.NSD_Database_get_ICMP_date_by_id(flow)
        pkt_date_before = datetime.strptime(pkts_date[0]['Date'], '%d/%m/%Y %H:%M:%S.%f')
        for pkt_date in pkts_date:
            pkt_date_next = datetime.strptime(pkt_date['Date'], '%d/%m/%Y %H:%M:%S.%f')
            diff = (pkt_date_next - pkt_date_before).total_seconds()*10000
            #self.logger.info(diff)
            if diff < 30:   
                datediff.append(diff)
            pkt_date_before = pkt_date_next
        #self.logger.info(str(datediff))
        date_diff_bef_norm = np.array(datediff)
        mean = np.mean(date_diff_bef_norm)
        std = np.std(date_diff_bef_norm)
        xx = []
        for c in date_diff_bef_norm:
            xx.append((c-mean)/std)
        x = np.array(xx)
        y = [0]*len(x)

        (counts, bins) = np.histogram(date_diff_bef_norm, bins=range(30))

        plt.figure(figsize=[10, 8])

        plt.bar(bins[:-1], counts, width=0.5, color='#0504aa', alpha=0.7)
        plt.xlim(min(bins), max(bins))
        plt.grid(axis='y', alpha=0.75)
        plt.xlabel('Value', fontsize=15)
        plt.ylabel('Frequency', fontsize=15)
        plt.xticks(fontsize=15)
        plt.yticks(fontsize=15)
        plt.ylabel('Frequency', fontsize=15)
        plt.title('Normal Distribution Histogram', fontsize=15)
        plt.show()

        #factor = 2
        #plt.hist(bins[:-1], bins, weights=factor * counts)
        #plt.hist2d(x, y, (50, 50), cmap=plt.cm.jet)
        #plt.colorbar()
        # Histogram of example data and normalized data
        #num_bins = 'auto'
        #n, bins, patches = plt.hist(date_diff_norm, num_bins, facecolor='blue', alpha=0.5)
        #n, bins, patches = plt.hist(x)
        #plt.scatter(x, y)
        #plt.show()
        """


    def NSD_AI_training(self, type_cc, prot, chats, packets, intervals):
        self.NSD_Flow_fork_database()

        self.logger.info('AI training starting...')
        data_training_set_Not_CC, intervals_Not_CC = self.NSD_AI_training_get_set(type_cc, prot, chats, packets, '')
        data_training_set_CC, intervals_CC = self.NSD_AI_training_get_set(type_cc, prot, chats, packets, '_CC')
        self.NSD_AI_training_PT1(chats, data_training_set_Not_CC, data_training_set_CC)
        #f = open("training_set_Not_CC_ICMP.txt", "a")
        #f.write(str(intervals))
        #f.write(str(data_training_set))
        #f.close()
        #exit(0)
        """
        data = []
        time.sleep(5)
        for flow in NSD_Monitor_Data.NSD_Monitor_Data_get_flows_ICMP():
            if NSD_Monitor_Data.NSD_Monitor_Data_get_status_flow_ICMP(flow[0]) != opts.FLOW_AI_TRAINED:
                self.NSD_AI_training_PT1(flow[0], data)
                flow_status = {
                    'Flow': opts.FLOW_FINISHED,
                    'AI': opts.FLOW_AI_FINISHED,
                    'Result': opts.FLOW_AI_TRAINED
                }
                NSD_Monitor_Data.NSD_Monitor_Data_update_status_flow_ICMP(flow[0], flow_status)
        """

