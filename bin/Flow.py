# Import python libraries
import logging

# Import local libraries
from bin.Database import Database
from bin.Monitor import Monitor_Data
from conf import variables as vrb


class Flow:

  def __init__(self, log_level, db_server, db_port, db_name, sync_queue):
    self.log_level = log_level
    self.logger = logging.getLogger(__name__)
    self.SQ = sync_queue
    self.db_server = db_server
    self.db_port = db_port
    self.db_name = db_name

  def Flow_fork_database(self):
    self.DB = Database(self.log_level, self.db_server, self.db_port, self.db_name, self.SQ)

  def Flow_get_flows(self, prot, tagged):
    flows_returned = []
    while True:
      for flow in getattr(self.DB, 'Database_get_' + prot + '_flows_id')(tagged):
        if flow not in flows_returned:
          flows_returned.append(flow)
          yield flow

  def Flow_ICMP(self, tagged):
    self.Flow_fork_database()
    flows = self.Flow_get_flows('ICMP', tagged)

    if self.log_level >= vrb.INFO:
      self.logger.debug('Flow_ICMP: get packets from database..')

    while True:
      flow = next(flows)

      # flow_id will be the objectID assigned by the database of the first packet inserted
      # The database will ensure it's the only one
      flow_id = str(flow[0]['_id'])

      # Update the status dict
      if Monitor_Data.Monitor_Data_get_status_flow_ICMP(flow_id) is None:
        flow_status = int(flow[0]['cc'])
        Monitor_Data.Monitor_Data_update_status_flow_ICMP(flow_id, flow_status)

      # Update counters
      Monitor_Data.Monitor_Data_update_counter_flow_ICMP(flow_id, len(flow))
      Monitor_Data.Monitor_Data_update_counter_flows_ICMP()

  def Flow_TCP(self, tagged):
    self.Flow_fork_database()

    if self.log_level >= vrb.INFO:
      self.logger.debug('Flow_TCP: get packets from database..')

    flows = self.Flow_get_flows('TCP', tagged)
    while True:
      flow = next(flows)

      # flow_id will be the objectID assigned by the database of the first packet inserted
      # The database will ensure it's the only one
      flow_id = str(flow[0]['_id'])

      # Update the status dict
      if Monitor_Data.Monitor_Data_get_status_flow_TCP(flow_id) is None:
        flow_status = int(flow[0]['cc'])
        Monitor_Data.Monitor_Data_update_status_flow_TCP(flow_id, flow_status)

      # Update counters
      Monitor_Data.Monitor_Data_update_counter_flow_TCP(flow_id, len(flow))
      Monitor_Data.Monitor_Data_update_counter_flows_TCP()

  def Flow_UDP(self, tagged):
    self.Flow_fork_database()

    if self.log_level >= vrb.INFO:
      self.logger.debug('Flow_UDP: get packets from database..')

    flows = self.Flow_get_flows('UDP', tagged)
    while True:
      flow = next(flows)

      # flow_id will be the objectID assigned by the database of the first packet inserted
      # The database will ensure it's the only one
      flow_id = str(flow[0]['_id'])

      # Update the status dict
      if Monitor_Data.Monitor_Data_get_status_flow_UDP(flow_id) is None:
        flow_status = int(flow[0]['cc'])
        Monitor_Data.Monitor_Data_update_status_flow_UDP(flow_id, flow_status)

      # Update counters
      Monitor_Data.Monitor_Data_update_counter_flow_UDP(flow_id, len(flow))
      Monitor_Data.Monitor_Data_update_counter_flows_UDP()

  def Flow_RTP(self, tagged):
    self.Flow_fork_database()

    if self.log_level >= vrb.INFO:
      self.logger.debug('Flow_RTP: get packets from database..')

    flows = self.Flow_get_flows('RTP', tagged)
    while True:
      flow = next(flows)

      # flow_id will be the objectID assigned by the database of the first packet inserted
      # The database will ensure it's the only one
      flow_id = str(flow[0]['_id'])

      if self.log_level >= vrb.DEBUG:
        self.logger.debug('Flow: RTP: flow id {}, category {}'.format(flow_id, flow[0]['cc']))

      # Update the status dict
      if Monitor_Data.Monitor_Data_get_status_flow_RTP(flow_id) is None:
        flow_status = int(flow[0]['cc'])
        Monitor_Data.Monitor_Data_update_status_flow_RTP(flow_id, flow_status)

      # Update counters
      Monitor_Data.Monitor_Data_update_counter_flow_RTP(flow_id, len(flow))
      Monitor_Data.Monitor_Data_update_counter_flows_RTP()
