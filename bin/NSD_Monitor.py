# Monitor class

# Imports python libraries
import time
import logging


# Class to monitor the app
class NSD_Monitor:

	# init method
	def __init__(self, log_level, counters, pipe):
		self.log_level = log_level
		self.logger = logging.getLogger(__name__)
		self.Counters = counters
		self.Pipe = pipe


	# monitor process
	def NSD_Monitor_process(self):
		while True:
			TCP_received_packets = self.Counters.NSD_Counters_get_total_received_TCP()
			UDP_received_packets = self.Counters.NSD_Counters_get_total_received_UDP()
			ICMP_received_packets = self.Counters.NSD_Counters_get_total_received_ICMP()
			TCP_database_packets = self.Counters.NSD_Counters_get_total_database_TCP()
			UDP_database_packets = self.Counters.NSD_Counters_get_total_database_UDP()
			ICMP_database_packets = self.Counters.NSD_Counters_get_total_database_ICMP()
			TCP_flows = self.Counters.NSD_Counters_get_flows_TCP()
			UDP_flows = self.Counters.NSD_Counters_get_flows_UDP()
			ICMP_flows = self.Counters.NSD_Counters_get_flows_ICMP()

			self.logger.info('\n\n--- PACKET PROCESS REPORT ---')
			self.logger.info('- TCP')
			self.logger.info('-- Received: ' + str(TCP_received_packets))
			self.logger.info('-- Inserted into database: ' + str(TCP_database_packets))
			self.logger.info('-- Flows:')
			self.logger.info('   +-------------------------+-----------+-------------------+')
			self.logger.info('   |           ID            |  Packets  |       STATUS      |')
			self.logger.info('   +-------------------------+-----------+-------------------+')
			for TCP_flow in TCP_flows:
				self.logger.info('   | ' + TCP_flow[0] + '|    ' + TCP_flow[1] + '   |' + TCP_flow[2] + '|')
			self.logger.info('   +-------------------------+-----------+-------------------+')
			self.logger.info('\n')
			self.logger.info('- UDP')
			self.logger.info('-- Received: ' + str(UDP_received_packets))
			self.logger.info('-- Inserted into database: ' + str(UDP_database_packets))
			self.logger.info('-- Flows:')
			self.logger.info('   +-------------------------+-----------+-------------------+')
			self.logger.info('   |           ID            |  Packets  |       STATUS      |')
			self.logger.info('   +-------------------------+-----------+-------------------+')
			for UDP_flow in UDP_flows:
				self.logger.info('   | ' + UDP_flow[0] + '|    ' + UDP_flow[1] + '   |' + UDP_flow[2] + '|')
			self.logger.info('   +-------------------------+-----------+-------------------+')
			self.logger.info('\n')
			self.logger.info('- ICMP')
			self.logger.info('-- Received: ' + str(ICMP_received_packets))
			self.logger.info('-- Inserted into database: ' + str(ICMP_database_packets))
			self.logger.info('-- Flows:')
			self.logger.info('   +-------------------------+-----------+-------------------+')
			self.logger.info('   |           ID            |  Packets  |       STATUS      |')
			self.logger.info('   +-------------------------+-----------+-------------------+')
			for ICMP_flow in ICMP_flows:
				self.logger.info('   | ' + ICMP_flow[0] + '|    ' + ICMP_flow[1] + '   |' + ICMP_flow[2] + '|')
			self.logger.info('   +-------------------------+-----------+-------------------+')
			self.logger.info('\n')

			if TCP_received_packets > TCP_database_packets:
				self.Pipe.send(['TCP', 1])
			if UDP_received_packets > UDP_database_packets:
				self.Pipe.send(['UDP', 1])
			if ICMP_received_packets > ICMP_database_packets:
				self.Pipe.send(['ICMP', 1])

			time.sleep(2)

