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

			self.logger.info('\n\n--- PACKET PROCESS REPORT ---')
			self.logger.info('- TCP')
			self.logger.info('-- Received: ' + str(TCP_received_packets))
			self.logger.info('-- Processed: ' + str(TCP_database_packets))
			self.logger.info('- UDP')
			self.logger.info('-- Received: ' + str(UDP_received_packets))
			self.logger.info('-- Processed: ' + str(UDP_database_packets))
			self.logger.info('- ICMP')
			self.logger.info('-- Received: ' + str(ICMP_received_packets))
			self.logger.info('-- Processed: ' + str(ICMP_database_packets))

			if TCP_received_packets > TCP_database_packets:
				self.Pipe.send(['TCP', 1])
			if UDP_received_packets > UDP_database_packets:
				self.Pipe.send(['UDP', 1])
			if ICMP_received_packets > ICMP_database_packets:
				self.Pipe.send(['ICMP', 1])

			time.sleep(2)

