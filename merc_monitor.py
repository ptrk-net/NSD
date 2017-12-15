# system libraries
import time

# Merc modules


# Class to monitor the app
class Merc_Monitor:

	# init method
	def __init__(self, counters, pipe):
		self.Counters = counters
		self.Pipe = pipe


	# monitor process
	def merc_monitor_process(self):
		while True:
			TCP_received_packets = self.Counters.merc_counters_get_received_TCP()
			UDP_received_packets = self.Counters.merc_counters_get_received_UDP()
			ICMP_received_packets = self.Counters.merc_counters_get_received_ICMP()
			TCP_processed_packets = self.Counters.merc_counters_get_received_TCP()
			UDP_processed_packets = self.Counters.merc_counters_get_received_UDP()
			ICMP_processed_packets = self.Counters.merc_counters_get_received_ICMP()

			print('\n\n--- PACKET PROCESS REPORT ---')
			print('- TCP')
			print('-- Received: ' + str(TCP_received_packets))
			print('-- Processed: ' + str(TCP_processed_packets))
			print('- UDP')
			print('-- Received: ' + str(UDP_received_packets))
			print('-- Processed: ' + str(UDP_processed_packets))
			print('- ICMP')
			print('-- Received: ' + str(ICMP_received_packets))
			print('-- Processed: ' + str(ICMP_processed_packets))

			if TCP_received_packets > TCP_processed_packets:
				self.Pipe.send(['TCP', 1])
			if UDP_received_packets > UDP_processed_packets:
				self.Pipe.send(['UDP', 1])
			if ICMP_received_packets > ICMP_processed_packets:
				self.Pipe.send(['ICMP', 1])

			time.sleep(2)

