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
        self.Flows_ICMP_status = {}
        self.Flows_TCP_status = {}
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

            #if self.log_level == 'DEBUG':
            #    self.logger.debug('NSD_Flow_flow_ICMP: .. done!')

            # Analyze each
            for flow in packets:
                # flow_id will be the objectID assigned by the database of the first packet inserted
                # The database will ensure it's the only one
                flow_id = flow[0]['_id']

                # Update the status dict
                if self.Flows_ICMP_status[flow_id] is None:
                    flow_status = {
                        'Flow': opts.FLOW_UPDATING,
                        'AI': opts.FLOW_AI_PS12_NOT_STARTED,
                        'Result': opts.FLOW_AI_PS12_SUSPECT
                    }
                    self.Flows_ICMP_status[flow_id] = flow_status

                # Update the counter
                self.Counters.NSD_Counters_update_flow_ICMP(flow_id, len(flow))

        # TODO
        # 1. Pass the packets to AI


    def NSD_Flow_TCP(self):
        self.NSD_Flow_fork_database()

        while True:
            if self.log_level == 'DEBUG':
                self.logger.debug('NSD_Flow_flow_TCP: get packets from database..')

            packets = []
            while not packets:
                time.sleep(2)
                packets = self.DB.NSD_Database_get_TCP_packets()

            #if self.log_level == 'DEBUG':
                #self.logger.debug('NSD_Flow_flow_TCP: .. done!')

            for flow in packets:
                # flow_id will be the objectID assigned by the database of the first packet inserted
                # The database will ensure it's the only one
                flow_id = flow[0]['_id']

                # Update the status dict
                if self.Flows_ICMP_status[flow_id] is None:
                    flow_status = {
                        'Flow': opts.FLOW_UPDATING,
                        'AI': opts.FLOW_AI_PS12_NOT_STARTED,
                        'Result': opts.FLOW_AI_PS12_SUSPECT
                    }
                    self.Flows_TCP_status[flow_id] = flow_status

                # Update the counter
                self.Counters.NSD_Counters_update_flow_TCP(flow_id, len(flow))

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

            #if self.log_level == 'DEBUG':
            #self.logger.debug('NSD_Flow_flow_TCP: .. done!')

            for flow in packets:
                # flow_id will be the objectID assigned by the database of the first packet inserted
                # The database will ensure it's the only one
                flow_id = flow[0]['_id']

                # Update the status dict
                if self.Flows_UDP_status[flow_id] is None:
                    flow_status = {
                        'Flow': opts.FLOW_UPDATING,
                        'AI': opts.FLOW_AI_PS12_NOT_STARTED,
                        'Result': opts.FLOW_AI_PS12_SUSPECT
                    }
                    self.Flows_UDP_status[flow_id] = flow_status

                # Update the counter
                self.Counters.NSD_Counters_update_flow_UDP(flow_id, len(flow))

        # TODO
        # 1. Pass the packets to AI
