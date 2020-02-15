# Import python libraries
from multiprocessing import Manager
import logging
import string
import random
import time

# Import NSD libraries
from bin.NSD_Database import NSD_Database
from bin.NSD_Monitor_Data import NSD_Monitor_Data
from bin.NSD_AI import NSD_AI
from conf import variables as opts


class NSD_Flow:

    def __init__(self, log_level, db_server, db_port, sync_queue):
        self.log_level = log_level
        self.logger = logging.getLogger(__name__)
        self.SQ = sync_queue
        self.db_server = db_server
        self.db_port = db_port

    def NSD_Flow_fork_database(self):
        self.DB = NSD_Database(self.log_level, self.db_server, self.db_port, self.SQ)  # MongoDB


    def NSD_Flow_ICMP(self):
        self.NSD_Flow_fork_database()

        while True:
            if self.log_level == 'DEBUG':
                self.logger.debug('NSD_Flow_flow_ICMP: get packets from database..')

            #flows = []
            #while not flows:
            flows = self.DB.NSD_Database_get_ICMP_packets()
            #   self.logger.info('XXXXXXXXXXXXXXXXXXXXXXXXX counter: ' + str(len(flows)))
            #    time.sleep(5)

            #if self.log_level == 'DEBUG':
            #    self.logger.debug('NSD_Flow_flow_ICMP: .. done!')

            # Analyze each
            for flow in flows:
                # flow_id will be the objectID assigned by the database of the first packet inserted
                # The database will ensure it's the only one
                flow_id = str(flow[0]['_id'])

                # Update the status dict
                if NSD_Monitor_Data.NSD_Monitor_Data_get_status_flow_ICMP(flow_id) is None:
                    flow_status = {
                        'Flow': opts.FLOW_UPDATING,
                        'AI': opts.FLOW_AI_NOT_STARTED,
                        'Result': opts.FLOW_AI_SUSPECT
                    }
                    NSD_Monitor_Data.NSD_Monitor_Data_update_status_flow_ICMP(flow_id, flow_status)

                # Update the counter
                NSD_Monitor_Data.NSD_Monitor_Data_update_counter_flow_ICMP(flow_id, len(flow))


    def NSD_Flow_TCP(self):
        self.NSD_Flow_fork_database()

        while True:
            if self.log_level == 'DEBUG':
                self.logger.debug('NSD_Flow_flow_TCP: get packets from database..')

            flows = []
            while not flows:
                time.sleep(2)
                flows = self.DB.NSD_Database_get_TCP_packets()

            #if self.log_level == 'DEBUG':
                #self.logger.debug('NSD_Flow_flow_TCP: .. done!')

            for flow in flows:
                # flow_id will be the objectID assigned by the database of the first packet inserted
                # The database will ensure it's the only one
                flow_id = str(flow[0]['_id'])

                # Update the status dict
                if NSD_Monitor_Data.NSD_Monitor_Data_get_status_flow_TCP(flow_id) is None:
                    flow_status = {
                        'Flow': opts.FLOW_UPDATING,
                        'AI': opts.FLOW_AI_NOT_STARTED,
                        'Result': opts.FLOW_AI_SUSPECT
                    }
                    NSD_Monitor_Data.NSD_Monitor_Data_update_status_flow_TCP(flow_id, flow_status)

                # Update the counter
                NSD_Monitor_Data.NSD_Monitor_Data_update_counter_flow_TCP(flow_id, len(flow))

        # TODO
        # 1. Pass the packets to AI

    def NSD_Flow_UDP(self):
        self.NSD_Flow_fork_database()

        while True:
            if self.log_level == 'DEBUG':
                self.logger.debug('NSD_Flow_flow_UDP: get packets from database..')

            flows = []
            while not flows:
                flows = self.DB.NSD_Database_get_UDP_packets()
                time.sleep(2)

            #if self.log_level == 'DEBUG':
            #self.logger.debug('NSD_Flow_flow_TCP: .. done!')

            for flow in flows:
                # flow_id will be the objectID assigned by the database of the first packet inserted
                # The database will ensure it's the only one
                flow_id = str(flow[0]['_id'])

                # Update the status dict
                if NSD_Monitor_Data.NSD_Monitor_Data_get_status_flow_UDP(flow_id) is None:
                    flow_status = {
                        'Flow': opts.FLOW_UPDATING,
                        'AI': opts.FLOW_AI_NOT_STARTED,
                        'Result': opts.FLOW_AI_SUSPECT
                    }
                    NSD_Monitor_Data.NSD_Monitor_Data_update_status_flow_TCP(flow_id, flow_status)

                # Update the counter
                NSD_Monitor_Data.NSD_Monitor_Data_update_counter_flow_UDP(flow_id, len(flow))

        # TODO
        # 1. Pass the packets to AI
