# Import python libraries
import logging

# Import local libraries
from bin.NSD_Database import NSD_Database
from bin.NSD_Monitor import NSD_Monitor_Data
from conf import variables as vrb


class NSD_Flow:

  def __init__(self, log_level, db_server, db_port, db_name, sync_queue):
    self.log_level = log_level
    self.logger = logging.getLogger(__name__)
    self.SQ = sync_queue
    self.db_server = db_server
    self.db_port = db_port
    self.db_name = db_name

  def fork_database(self):
    self.DB = NSD_Database(self.log_level, self.db_server, self.db_port, self.db_name, self.SQ)

  def get_flows(self, prot, tagged):
    flows_returned = []
    while True:
      for flow in getattr(self.DB, 'get_' + prot + '_flows_id')(tagged):
        if flow not in flows_returned:
          flows_returned.append(flow)
          yield flow

  def get_flow_ICMP(self, tagged):
    self.fork_database()
    flows = self.get_flows('ICMP', tagged)

    if self.log_level >= vrb.INFO:
      self.logger.debug('Flow_ICMP: get packets from database..')

    while True:
      flow = next(flows)

      # flow_id will be the objectID assigned by the database of the first packet inserted
      # The database will ensure it's the only one
      flow_id = str(flow[0]['_id'])

      # Update the status dict
      if NSD_Monitor_Data.get_status_flow_ICMP(flow_id) is None:
        flow_status = int(flow[0]['cc'])
        NSD_Monitor_Data.update_status_flow_ICMP(flow_id, flow_status)

      # Update counters
      NSD_Monitor_Data.update_counter_flow_ICMP(flow_id, len(flow))
      NSD_Monitor_Data.update_counter_flows_ICMP()

  def get_flow_TCP(self, tagged):
    self.fork_database()

    if self.log_level >= vrb.INFO:
      self.logger.debug('get_flow_TCP: get packets from database..')

    flows = self.get_flows('TCP', tagged)
    while True:
      flow = next(flows)

      # flow_id will be the objectID assigned by the database of the first packet inserted
      # The database will ensure it's the only one
      flow_id = str(flow[0]['_id'])

      # Update the status dict
      if NSD_Monitor_Data.get_status_flow_TCP(flow_id) is None:
        flow_status = int(flow[0]['cc'])
        NSD_Monitor_Data.update_status_flow_TCP(flow_id, flow_status)

      # Update counters
      NSD_Monitor_Data.update_counter_flow_TCP(flow_id, len(flow))
      NSD_Monitor_Data.update_counter_flows_TCP()

  def get_flow_UDP(self, tagged):
    self.fork_database()

    if self.log_level >= vrb.INFO:
      self.logger.debug('get_flow_UDP: get packets from database..')

    flows = self.get_flows('UDP', tagged)
    while True:
      flow = next(flows)

      # flow_id will be the objectID assigned by the database of the first packet inserted
      # The database will ensure it's the only one
      flow_id = str(flow[0]['_id'])

      # Update the status dict
      if NSD_Monitor_Data.get_status_flow_UDP(flow_id) is None:
        flow_status = int(flow[0]['cc'])
        NSD_Monitor_Data.update_status_flow_UDP(flow_id, flow_status)

      # Update counters
      NSD_Monitor_Data.update_counter_flow_UDP(flow_id, len(flow))
      NSD_Monitor_Data.update_counter_flows_UDP()

  def get_flow_RTP(self, tagged):
    self.fork_database()

    if self.log_level >= vrb.INFO:
      self.logger.debug('get_flow_RTP: get packets from database..')

    flows = self.get_flows('RTP', tagged)
    while True:
      flow = next(flows)

      # flow_id will be the objectID assigned by the database of the first packet inserted
      # The database will ensure it's the only one
      flow_id = str(flow[0]['_id'])
      rt_counter = len(flow)

      if self.log_level >= vrb.DEBUG:
        self.logger.debug('NSD_Flow: get RTP: flow id {}, category {}'.format(flow_id, flow[0]['cc']))

      # Update the status dict
      flow_status = NSD_Monitor_Data.get_status_flow_RTP(flow_id)
      if flow_status is None:
        #flow_status = int(flow[0]['cc'])
        NSD_Monitor_Data.update_status_flow_RTP(flow_id,
                                                [vrb.FLOW_UPDATING, vrb.FLOW_ML_NOT_STARTED, vrb.FLOW_ML_SUSPECT])
      else:
        if flow_status[0] == vrb.FLOW_FINISHED and flow_status[1] == vrb.FLOW_ML_FINISHED:
          NSD_Monitor_Data.delete_flow_RTP(flow_id)
        elif flow_status[0] == vrb.FLOW_UPDATING:
          if rt_counter == NSD_Monitor_Data.get_counter_flow_RTP(flow_id):
            NSD_Monitor_Data.update_status_flow_RTP(flow_id,
                                                    [vrb.FLOW_FINISHED, flow_status[1], flow_status[2]])
          else:
            # Update counters
            NSD_Monitor_Data.update_counter_flow_RTP(flow_id, rt_counter)
            NSD_Monitor_Data.update_counter_flows_RTP()


  def control_RTP_flows(self):
    self.fork_database()

    if self.log_level >= vrb.INFO:
      self.logger.debug('control_RTP_flows: starting..')

    flows = self.get_flows('RTP', tagged)
    while True:
      flow = next(flows)
      flow_id = str(flow[0]['_id'])

      if self.log_level >= vrb.DEBUG:
        self.logger.debug('NSD_Flow: RTP: flow id {}, category {}'.format(flow_id, flow[0]['cc']))

      flow_status = NSD_Monitor_Data.get_status_flow_RTP(flow_id)

      if flow_status[0] == FLOW_FINISHED and status[1] == FLOW_ML_FINISHED:
        if self.log_level >= vrb.INFO:
          self.logger.debug('NSD_Flow: control RTP: flow id {} to be deleted'.format(flow_id))

        # delete from database
        # delete from Monitor_Data


