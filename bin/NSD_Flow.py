# Import python libraries
import logging
import string
import random
import time

# Import NSD libraries
from bin.NSD_Database import NSD_Database
from conf import variables as opts


class NSD_Flow:

    def __init__(self, log_level, db_server, db_port, counters, sync_queue):
        self.log_level = log_level
        self.logger = logging.getLogger(__name__)
        self.Counters = counters
        self.SQ = sync_queue
        self.db_server = db_server
        self.db_port = db_port

        # variables to maintain a local bbdd with flows processing
        self.Flows_ICMP_id = {}
        self.Flows_ICMP_status = {}
        self.Flows_TCP_id = {}
        self.Flows_TCP_status = {}
        self.Flows_UDP_id = {}
        self.Flows_UDP_status = {}

    def NSD_Flow_fork_database(self):
        self.DB = NSD_Database(self.log_level, self.db_server, self.db_port, self.SQ)  # MongoDB

    def NSD_Flow_ICMP(self):
        self.NSD_Flow_fork_database()

        while True:
            if self.log_level == 'DEBUG':
                self.logger.debug('NSD_Flow_flow_ICMP: get packets from database..')

            packets = 'None'
            while packets == 'None':
                packets = self.DB.NSD_Database_get_ICMP_packets()
                time.sleep(2)

            if self.log_level == 'DEBUG':
                self.logger.debug('NSD_Flow_flow_ICMP: .. done!')

            # get the flow ID
            key = str(packets["Source_IP"] + '-' + packets["Dest_IP"])
            flow_id = self.Flows_ICMP_id.get(key)
            if flow_id == 'None':
                flow_id = 'ICMP_' + ''.join(
                    random.choices(string.ascii_letters + string.digits + string.punctuation, k=25))

            # Update the id dict
            self.Flows_ICMP_id.update([key, flow_id])

            # Update the status dict
            flow_status = {
                'Flow': opts.FLOW_UPDATING,
                'AI': opts.FLOW_AI_PS12_NOT_STARTED,
                'Result': opts.FLOW_AI_PS12_SUSPECT
            }
            self.Flows_ICMP_status.update([flow_id, flow_status])

            # Update the counter
            self.Counters.NSD_Counters_update_flow_ICMP(flow_id, packets.len())

        # TODO
        # 1. Pass the packets to AI

    def NSD_Flow_TCP(self):
        self.NSD_Flow_fork_database()

        while True:
            if self.log_level == 'DEBUG':
                self.logger.debug('NSD_Flow_flow_TCP: get packets from database..')

            packets = 'None'
            while packets == 'None':
                packets = self.DB.NSD_Database_get_TCP_packets()
                time.sleep(2)

            if self.log_level == 'DEBUG':
                self.logger.debug('NSD_Flow_flow_ICMP: .. done!')

            # get the flow ID
            key = str(packets["Source_IP"] + '-' + packets["Source_Port"] + '-' +
                      packets["Dest_IP"] + '-' + packets["Dest_Port"])
            flow_id = self.Flows_TCP_id.get(key)
            if flow_id == 'None':
                flow_id = 'TCP_' + ''.join(
                    random.choices(string.ascii_letters + string.digits + string.punctuation, k=25))

            # Update the id dict
            self.Flows_TCP_id.update([key, flow_id])

            # Update the status dict
            flow_status = {
                'Flow': opts.FLOW_UPDATING,
                'AI': opts.FLOW_AI_PS12_NOT_STARTED,
                'Result': opts.FLOW_AI_PS12_SUSPECT
            }
            self.Flows_TCP_status.update([flow_id, flow_status])

            # Update the counter
            self.Counters.NSD_Counters_update_flow_TCP(flow_id, packets.len())

        # TODO
        # 1. Pass the packets to AI

    def NSD_Flow_UDP(self):
        self.NSD_Flow_fork_database()

        while True:
            if self.log_level == 'DEBUG':
                self.logger.debug('NSD_Flow_flow_UDP: get packets from database..')

            packets = 'None'
            while packets == 'None':
                packets = self.DB.NSD_Database_get_UDP_packets()
                time.sleep(2)

            if self.log_level == 'DEBUG':
                self.logger.debug('NSD_Flow_flow_UDP: .. done!')

            # get the flow ID
            key = str(packets["Source_IP"] + '-' + packets["Source_Port"] + '-' +
                      packets["Dest_IP"] + '-' + packets["Dest_Port"])
            flow_id = self.Flows_UDP_id.get(key)
            if flow_id == 'None':
                flow_id = 'UDP_' + ''.join(
                    random.choices(string.ascii_letters + string.digits + string.punctuation, k=25))

            # Update the id dict
            self.Flows_UDP_id.update([key, flow_id])

            # Update the status dict
            flow_status = {
                'Flow': opts.FLOW_UPDATING,
                'AI': opts.FLOW_AI_PS12_NOT_STARTED,
                'Result': opts.FLOW_AI_PS12_SUSPECT
            }
            self.Flows_UDP_status.update([flow_id, flow_status])

            # Update the counter
            self.Counters.NSD_Counters_update_flow_UDP(flow_id, packets.len())

            self.logger.info(str(self.Flows_UDP_id))
            self.logger.info(str(self.Flows_UDP_status))
            self.logger.info(str(packets))

        # TODO
        # 1. Pass the packets to AI
