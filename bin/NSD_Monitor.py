# Monitor class

# Imports python libraries
import time
import logging

# Import NSD libraries
from bin.NSD_Monitor_Data import NSD_Monitor_Data


# Class to monitor the app
class NSD_Monitor:

    # init method
    def __init__(self, log_level, pipe, sync_queue):
        self.log_level = log_level
        self.logger = logging.getLogger(__name__)
        self.SQ = sync_queue
        self.Pipe = pipe
        self.__status_matrix = [['FLOW', ['UPDATING', 'STANDBY', 'FINISHED', 'ARCHIVED']],
                                ['AI', ['NOT_STARTED',
                                        'PT1_WORKING', 'PT1_WAITING', 'PT1_FINISHED',
                                        'PS12_WORKING', 'PS12_WAITING', 'PS12_FINISHED',
                                        ]],
                                ['RESULT', ['POSITIVE', 'NEGATIVE', 'SUSPECT']]]

    # Return the string that identifies a status
    # TODO: it's manually done, should be read from 'variables' file
    def __NSD_Monitor_get_name_status(self, type_status, status):
        return str(self.__status_matrix[type_status][0] + ': ' + self.__status_matrix[type_status][1][status])

    # monitor process
    def NSD_Monitor_process(self, pcap=False):
        if self.log_level != 'DEBUG':
            return 0

        while True:
            TCP_received_packets = NSD_Monitor_Data.NSD_Monitor_Data_get_total_received_TCP()
            UDP_received_packets = NSD_Monitor_Data.NSD_Monitor_Data_get_total_received_UDP()
            ICMP_received_packets = NSD_Monitor_Data.NSD_Monitor_Data_get_total_received_ICMP()
            TCP_database_packets = NSD_Monitor_Data.NSD_Monitor_Data_get_total_database_TCP()
            UDP_database_packets = NSD_Monitor_Data.NSD_Monitor_Data_get_total_database_UDP()
            ICMP_database_packets = NSD_Monitor_Data.NSD_Monitor_Data_get_total_database_ICMP()
            TCP_flows = NSD_Monitor_Data.NSD_Monitor_Data_get_flows_TCP()
            UDP_flows = NSD_Monitor_Data.NSD_Monitor_Data_get_flows_UDP()
            ICMP_flows = NSD_Monitor_Data.NSD_Monitor_Data_get_flows_ICMP()

            self.logger.info('------------------------ PACKET PROCESS REPORT -------------------------')
            self.logger.info('- TCP')
            self.logger.info('-- Received: ' + str(TCP_received_packets))
            self.logger.info('-- Inserted into database: ' + str(TCP_database_packets))
            self.logger.info('-- Flows:')
            self.logger.info('   +--------------------------+-----------+----------------------------+')
            self.logger.info('   |           ID             |  Packets  |            STATUS          |')
            self.logger.info('   +--------------------------+-----------+----------------------------+')
            for TCP_flow in TCP_flows:
                self.logger.info('   | ' + TCP_flow[0] + ' |    ' + str(TCP_flow[1]) + '     |    FLOW: ' +
                                 str(self.__status_matrix[0][1][TCP_flow[2]['Flow']]) + '   |')
                self.logger.info('   |                          |           |    AI: ' +
                                 str(self.__status_matrix[1][1][TCP_flow[2]['AI']]) + '   |')
                self.logger.info('   |                          |           |    RESULT: ' +
                                 str(self.__status_matrix[2][1][TCP_flow[2]['Result']]) + '   |')
            self.logger.info('   +--------------------------+-----------+----------------------------+')
            self.logger.info('')
            self.logger.info('- UDP')
            self.logger.info('-- Received: ' + str(UDP_received_packets))
            self.logger.info('-- Inserted into database: ' + str(UDP_database_packets))
            self.logger.info('-- Flows:')
            self.logger.info('   +--------------------------+-----------+----------------------------+')
            self.logger.info('   |           ID             |  Packets  |            STATUS          |')
            self.logger.info('   +--------------------------+-----------+----------------------------+')
            for UDP_flow in UDP_flows:
                self.logger.info('   | ' + UDP_flow[0] + ' |    ' + str(UDP_flow[1]) + '     |    FLOW: ' +
                                 str(self.__status_matrix[0][1][UDP_flow[2]['Flow']]) + '   |')
                self.logger.info('   |                          |           |    AI: ' +
                                 str(self.__status_matrix[1][1][UDP_flow[2]['AI']]) + '   |')
                self.logger.info('   |                          |           |    RESULT: ' +
                                 str(self.__status_matrix[2][1][UDP_flow[2]['Result']]) + '   |')
            self.logger.info('   +--------------------------+-----------+----------------------------+')
            self.logger.info('')
            self.logger.info('- ICMP')
            self.logger.info('-- Received: ' + str(ICMP_received_packets))
            self.logger.info('-- Inserted into database: ' + str(ICMP_database_packets))
            self.logger.info('-- Flows:')
            self.logger.info('   +--------------------------+-----------+----------------------------+')
            self.logger.info('   |           ID             |  Packets  |            STATUS          |')
            self.logger.info('   +--------------------------+-----------+----------------------------+')
            for ICMP_flow in ICMP_flows:
                self.logger.info('   | ' + ICMP_flow[0] + ' |    ' + str(ICMP_flow[1]) + '     |    FLOW: ' +
                                 str(self.__status_matrix[0][1][ICMP_flow[2]['Flow']]) + '   |')
                self.logger.info('   |                          |           |    AI: ' +
                                 str(self.__status_matrix[1][1][ICMP_flow[2]['AI']]) + '   |')
                self.logger.info('   |                          |           |    RESULT: ' +
                                 str(self.__status_matrix[2][1][ICMP_flow[2]['Result']]) + '   |')
            self.logger.info('   +--------------------------+-----------+----------------------------+')
            self.logger.info('')

            if ICMP_received_packets == ICMP_database_packets:
                self.SQ.put('DATA_PROCESSED')
                if pcap:
                    self.SQ.put('KILL')
                    #exit(0)

            if TCP_received_packets > TCP_database_packets:
                self.Pipe.send(['TCP', 1])
            if UDP_received_packets > UDP_database_packets:
                self.Pipe.send(['UDP', 1])
            if ICMP_received_packets > ICMP_database_packets:
                self.Pipe.send(['ICMP', 1])

            time.sleep(2)
