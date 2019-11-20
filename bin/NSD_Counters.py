# Class to count the packets received and processed

# Imports python libraries
from multiprocessing import Value, Lock
import logging

class NSD_Counters:
	def __init__(self, log_level, initial_value = 0):
		self.log_level = log_level
		self.logger = logging.getLogger(__name__)
		self.lock = Lock()

		self.Received_Counter_HOPOPTS = Value('i', initial_value)
		self.Received_Counter_IP = Value('i', initial_value)
		self.Received_Counter_ICMP = Value('i', initial_value)
		self.Received_Counter_IGMP = Value('i', initial_value)
		self.Received_Counter_SCTP = Value('i', initial_value)
		self.Received_Counter_TCP = Value('i', initial_value)
		self.Received_Counter_EGP = Value('i', initial_value)
		self.Received_Counter_PUP = Value('i', initial_value)
		self.Received_Counter_UDP = Value('i', initial_value)
		self.Received_Counter_IDP = Value('i', initial_value)
		self.Received_Counter_IPIP = Value('i', initial_value)
		self.Received_Counter_TP = Value('i', initial_value)
		self.Received_Counter_PIM = Value('i', initial_value)
		self.Received_Counter_IPV6 = Value('i', initial_value)
		self.Received_Counter_ROUTING = Value('i', initial_value)
		self.Received_Counter_FRAGMENT = Value('i', initial_value)
		self.Received_Counter_RSVP = Value('i', initial_value)
		self.Received_Counter_GRE = Value('i', initial_value)
		self.Received_Counter_ESP = Value('i', initial_value)
		self.Received_Counter_AH = Value('i', initial_value)
		self.Received_Counter_ICMPV6 = Value('i', initial_value)
		self.Received_Counter_NONE = Value('i', initial_value)
		self.Received_Counter_DSTOPTS = Value('i', initial_value)
		self.Received_Counter_RAW = Value('i', initial_value)
		self.Received_Counter_SSCOPMCE = Value('i', initial_value)

		self.Processed_Counter_HOPOPTS = Value('i', initial_value)
		self.Processed_Counter_IP = Value('i', initial_value)
		self.Processed_Counter_ICMP = Value('i', initial_value)
		self.Processed_Counter_IGMP = Value('i', initial_value)
		self.Processed_Counter_SCTP = Value('i', initial_value)
		self.Processed_Counter_TCP = Value('i', initial_value)
		self.Processed_Counter_EGP = Value('i', initial_value)
		self.Processed_Counter_PUP = Value('i', initial_value)
		self.Processed_Counter_UDP = Value('i', initial_value)
		self.Processed_Counter_IDP = Value('i', initial_value)
		self.Processed_Counter_IPIP = Value('i', initial_value)
		self.Processed_Counter_TP = Value('i', initial_value)
		self.Processed_Counter_PIM = Value('i', initial_value)
		self.Processed_Counter_IPV6 = Value('i', initial_value)
		self.Processed_Counter_ROUTING = Value('i', initial_value)
		self.Processed_Counter_FRAGMENT = Value('i', initial_value)
		self.Processed_Counter_RSVP = Value('i', initial_value)
		self.Processed_Counter_GRE = Value('i', initial_value)
		self.Processed_Counter_ESP = Value('i', initial_value)
		self.Processed_Counter_AH = Value('i', initial_value)
		self.Processed_Counter_ICMPV6 = Value('i', initial_value)
		self.Processed_Counter_NONE = Value('i', initial_value)
		self.Processed_Counter_DSTOPTS = Value('i', initial_value)
		self.Processed_Counter_RAW = Value('i', initial_value)
		self.Processed_Counter_SSCOPMCE = Value('i', initial_value)


	# Process
	def NSD_Counters_increment_received_HOPOPTS(self):
		with self.lock:
			self.Received_Counter_HOPOPTS.value += 1

	def NSD_Counters_increment_received_IP(self):
		with self.lock:
			self.Received_Counter_IP.value += 1

	def NSD_Counters_increment_received_ICMP(self):
		with self.lock:
			self.Received_Counter_ICMP.value += 1

	def NSD_Counters_increment_received_IGMP(self):
		with self.lock:
			self.Received_Counter_IGMP.value += 1

	def NSD_Counters_increment_received_SCTP(self):
		with self.lock:
			self.Received_Counter_SCTP.value += 1

	def NSD_Counters_increment_received_TCP(self):
		with self.lock:
			self.Received_Counter_TCP.value += 1

	def NSD_Counters_increment_received_EGP(self):
		with self.lock:
			self.Received_Counter_EGP.value += 1

	def NSD_Counters_increment_received_PUP(self):
		with self.lock:
			self.Received_Counter_PUP.value += 1

	def NSD_Counters_increment_received_UDP(self):
		with self.lock:
			self.Received_Counter_UDP.value += 1

	def NSD_Counters_increment_received_IDP(self):
		with self.lock:
			self.Received_Counter_IDP.value += 1

	def NSD_Counters_increment_received_IPIP(self):
		with self.lock:
			self.Received_Counter_IPIP.value += 1

	def NSD_Counters_increment_received_TP(self):
		with self.lock:
			self.Received_Counter_TP.value += 1

	def NSD_Counters_increment_received_PIM(self):
		with self.lock:
			self.Received_Counter_PIM.value += 1

	def NSD_Counters_increment_received_IPV6(self):
		with self.lock:
			self.Received_Counter_IPV6.value += 1

	def NSD_Counters_increment_received_ROUTING(self):
		with self.lock:
			self.Received_Counter_ROUTING.value += 1

	def NSD_Counters_increment_received_FRAGMENT(self):
		with self.lock:
			self.Received_Counter_FRAGMENT.value += 1

	def NSD_Counters_increment_received_SSCOPMCE(self):
		with self.lock:
			self.Received_Counter_SSCOPMCE.value += 1

	def NSD_Counters_increment_processed_HOPOPTS(self):
		with self.lock:
			self.Processed_Counter_HOPOPTS.value += 1

	def NSD_Counters_increment_processed_IP(self):
		with self.lock:
			self.Processed_Counter_IP.value += 1

	def NSD_Counters_increment_processed_ICMP(self):
		with self.lock:
			self.Processed_Counter_ICMP.value += 1

	def NSD_Counters_increment_processed_IGMP(self):
		with self.lock:
			self.Processed_Counter_IGMP.value += 1

	def NSD_Counters_increment_processed_SCTP(self):
		with self.lock:
			self.Processed_Counter_SCTP.value += 1

	def NSD_Counters_increment_processed_TCP(self):
		with self.lock:
			self.Processed_Counter_TCP.value += 1

	def NSD_Counters_increment_processed_EGP(self):
		with self.lock:
			self.Processed_Counter_EGP.value += 1

	def NSD_Counters_increment_processed_PUP(self):
		with self.lock:
			self.Processed_Counter_PUP.value += 1

	def NSD_Counters_increment_processed_UDP(self):
		with self.lock:
			self.Processed_Counter_UDP.value += 1

	def NSD_Counters_increment_processed_IDP(self):
		with self.lock:
			self.Processed_Counter_IDP.value += 1

	def NSD_Counters_increment_processed_IPIP(self):
		with self.lock:
			self.Processed_Counter_IPIP.value += 1

	def NSD_Counters_increment_processed_TP(self):
		with self.lock:
			self.Processed_Counter_TP.value += 1

	def NSD_Counters_increment_processed_PIM(self):
		with self.lock:
			self.Processed_Counter_PIM.value += 1

	def NSD_Counters_increment_processed_IPV6(self):
		with self.lock:
			self.Processed_Counter_IPV6.value += 1

	def NSD_Counters_increment_processed_ROUTING(self):
		with self.lock:
			self.Processed_Counter_ROUTING.value += 1

	def NSD_Counters_increment_processed_FRAGMENT(self):
		with self.lock:
			self.Processed_Counter_FRAGMENT.value += 1

	def NSD_Counters_increment_processed_SSCOPMCE(self):
		with self.lock:
			self.Processed_Counter_SSCOPMCE.value += 1

	# Get counters
	def NSD_Counters_get_received_HOPOPTS(self):
		with self.lock:
			return self.Received_Counter_HOPOPTS.value

	def NSD_Counters_get_received_IP(self):
		with self.lock:
			return self.Received_Counter_IP.value

	def NSD_Counters_get_received_ICMP(self):
		with self.lock:
			return self.Received_Counter_ICMP.value

	def NSD_Counters_get_received_IGMP(self):
		with self.lock:
			return self.Received_Counter_IGMP.value

	def NSD_Counters_get_received_SCTP(self):
		with self.lock:
			return self.Received_Counter_SCTP.value

	def NSD_Counters_get_received_TCP(self):
		with self.lock:
			return self.Received_Counter_TCP.value

	def NSD_Counters_get_received_EGP(self):
		with self.lock:
			return self.Received_Counter_EGP.value

	def NSD_Counters_get_received_PUP(self):
		with self.lock:
			return self.Received_Counter_PUP.value

	def NSD_Counters_get_received_UDP(self):
		with self.lock:
			return self.Received_Counter_UDP.value

	def NSD_Counters_get_received_IDP(self):
		with self.lock:
			return self.Received_Counter_IDP.value

	def NSD_Counters_get_received_IPIP(self):
		with self.lock:
			return self.Received_Counter_IPIP.value

	def NSD_Counters_get_received_TP(self):
		with self.lock:
			return self.Received_Counter_TP.value

	def NSD_Counters_get_received_PIM(self):
		with self.lock:
			return self.Received_Counter_PIM.value

	def NSD_Counters_get_received_IPV6(self):
		with self.lock:
			return self.Received_Counter_IPV6.value

	def NSD_Counters_get_received_ROUTING(self):
		with self.lock:
			return self.Received_Counter_ROUTING.value

	def NSD_Counters_get_received_FRAGMENT(self):
		with self.lock:
			return self.Received_Counter_FRAGMENT.value

	def NSD_Counters_get_received_RSVP(self):
		with self.lock:
			return self.Received_Counter_RSVP.value

	def NSD_Counters_get_received_SSCOPMCE(self):
		with self.lock:
			return self.Received_Counter_SSCOPMCE.value

	def NSD_Counters_get_processed_HOPOPTS(self):
		with self.lock:
			return self.Processed_Counter_HOPOPTS.value

	def NSD_Counters_get_processed_IP(self):
		with self.lock:
			return self.Processed_Counter_IP.value

	def NSD_Counters_get_processed_ICMP(self):
		with self.lock:
			return self.Processed_Counter_ICMP.value

	def NSD_Counters_get_processed_IGMP(self):
		with self.lock:
			return self.Processed_Counter_IGMP.value

	def NSD_Counters_get_processed_SCTP(self):
		with self.lock:
			return self.Processed_Counter_SCTP.value

	def NSD_Counters_get_processed_TCP(self):
		with self.lock:
			return self.Processed_Counter_TCP.value

	def NSD_Counters_get_processed_EGP(self):
		with self.lock:
			return self.Processed_Counter_EGP.value

	def NSD_Counters_get_processed_PUP(self):
		with self.lock:
			return self.Processed_Counter_PUP.value

	def NSD_Counters_get_processed_UDP(self):
		with self.lock:
			return self.Processed_Counter_UDP.value

	def NSD_Counters_get_processed_IDP(self):
		with self.lock:
			return self.Processed_Counter_IDP.value

	def NSD_Counters_get_processed_IPIP(self):
		with self.lock:
			return self.Processed_Counter_IPIP.value

	def NSD_Counters_get_processed_TP(self):
		with self.lock:
			return self.Processed_Counter_TP.value

	def NSD_Counters_get_processed_PIM(self):
		with self.lock:
			return self.Processed_Counter_PIM.value

	def NSD_Counters_get_processed_IPV6(self):
		with self.lock:
			return self.Processed_Counter_IPV6.value

	def NSD_Counters_get_processed_ROUTING(self):
		with self.lock:
			return self.Processed_Counter_ROUTING.value

	def NSD_Counters_get_processed_FRAGMENT(self):
		with self.lock:
			return self.Processed_Counter_FRAGMENT.value

	def NSD_Counters_get_processed_RSVP(self):
		with self.lock:
			return self.Processed_Counter_RSVP.value

	def NSD_Counters_get_processed_SSCOPMCE(self):
		with self.lock:
			return self.Processed_Counter_SSCOPMCE.value


