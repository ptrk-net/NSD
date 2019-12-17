# Monitor class

# Imports python libraries
import time
import logging

# Import NSD libraries
from bin.NSD_Counters import NSD_Counters


# Class to monitor the app
class NSD_Monitor:

    # init method
    def __init__(self, log_level, pipe):
        self.log_level = log_level
        self.logger = logging.getLogger(__name__)
        self.Pipe = pipe

    # monitor process
    def NSD_Monitor_process(self):
        while True:
            TCP_received_packets = NSD_Counters.NSD_Counters_get_total_received_TCP()
            UDP_received_packets = NSD_Counters.NSD_Counters_get_total_received_UDP()
            ICMP_received_packets = NSD_Counters.NSD_Counters_get_total_received_ICMP()
            TCP_database_packets = NSD_Counters.NSD_Counters_get_total_database_TCP()
            UDP_database_packets = NSD_Counters.NSD_Counters_get_total_database_UDP()
            ICMP_database_packets = NSD_Counters.NSD_Counters_get_total_database_ICMP()
            TCP_flows = dict(NSD_Counters.Counter_Flows_TCP)
            UDP_flows = dict(NSD_Counters.Counter_Flows_UDP)
            ICMP_flows = dict(NSD_Counters.Counter_Flows_ICMP)

            self.logger.info('------------------- PACKET PROCESS REPORT --------------------')
            self.logger.info('- TCP')
            self.logger.info('-- Received: ' + str(TCP_received_packets))
            self.logger.info('-- Inserted into database: ' + str(TCP_database_packets))
            self.logger.info('-- Flows:')
            self.logger.info('   +--------------------------+-----------+-------------------+')
            self.logger.info('   |           ID             |  Packets  |       STATUS      |')
            self.logger.info('   +--------------------------+-----------+-------------------+')
            for TCP_flow in TCP_flows:
                self.logger.info('   | ' + TCP_flow + ' |    ' + str(TCP_flows[TCP_flow]) +
                                 '     |         0         |')
            self.logger.info('   +--------------------------+-----------+-------------------+')
            self.logger.info('')
            self.logger.info('- UDP')
            self.logger.info('-- Received: ' + str(UDP_received_packets))
            self.logger.info('-- Inserted into database: ' + str(UDP_database_packets))
            self.logger.info('-- Flows:')
            self.logger.info('   +--------------------------+-----------+-------------------+')
            self.logger.info('   |           ID             |  Packets  |       STATUS      |')
            self.logger.info('   +--------------------------+-----------+-------------------+')
            for UDP_flow in UDP_flows:
                self.logger.info('   | ' + UDP_flow + ' |    ' + str(UDP_flows[UDP_flow]) +
                                 '     |         0         |')
            self.logger.info('   +--------------------------+-----------+-------------------+')
            self.logger.info('')
            self.logger.info('- ICMP')
            self.logger.info('-- Received: ' + str(ICMP_received_packets))
            self.logger.info('-- Inserted into database: ' + str(ICMP_database_packets))
            self.logger.info('-- Flows:')
            self.logger.info('   +--------------------------+-----------+-------------------+')
            self.logger.info('   |           ID             |  Packets  |       STATUS      |')
            self.logger.info('   +--------------------------+-----------+-------------------+')
            for ICMP_flow in ICMP_flows:
                self.logger.info('   | ' + ICMP_flow + ' |    ' + str(ICMP_flows[ICMP_flow]) +
                                 '     |         0         |')
            self.logger.info('   +--------------------------+-----------+-------------------+')
            self.logger.info('')

            if TCP_received_packets > TCP_database_packets:
                self.Pipe.send(['TCP', 1])
            if UDP_received_packets > UDP_database_packets:
                self.Pipe.send(['UDP', 1])
            if ICMP_received_packets > ICMP_database_packets:
                self.Pipe.send(['ICMP', 1])

            time.sleep(2)
