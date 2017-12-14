# system libraries
from multiprocessing import Value, Lock

class Merc_Counters:
	def __init__(self, initial_value = 0):

		self.lock = Lock()

		self.Received_Lock_TCP = Lock()
		self.Received_Lock_UDP = Lock()
		self.Received_Lock_ICMP = Lock()

		self.Processed_Lock_TCP = Lock()
		self.Processed_Lock_UDP = Lock()
		self.Processed_Lock_ICMP = Lock()

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


	# Process
	def merc_counters_increment_received_HOPOPTS(self):
		with self.lock:
			self.Received_Counter_HOPOPTS += 1

	def merc_counters_increment_received_IP(self):
		with self.lock:
			self.Received_Counter_IP += 1

	def merc_counters_increment_received_ICMP(self):
		with self.Received_Lock_ICMP:
			self.Received_Counter_ICMP += 1

	def merc_counters_increment_received_IGMP(self):
		with self.lock:
			self.Received_Counter_IGMP += 1

	def merc_counters_increment_received_SCTP(self):
		with self.lock:
			self.Received_Counter_SCTP += 1

	def merc_counters_increment_received_TCP(self):
		with self.Received_Lock_TCP:
			self.Received_Counter_TCP += 1

	def merc_counters_increment_received_EGP(self):
		with self.lock:
			self.Received_Counter_EGP += 1

	def merc_counters_increment_received_PUP(self):
		with self.lock:
			self.Received_Counter_PUP += 1

	def merc_counters_increment_received_UDP(self):
		with self.Received_Lock_UDP:
			self.Received_Counter_UDP += 1

	def merc_counters_increment_received_IDP(self):
		with self.lock:
			self.Received_Counter_IDP += 1

	def merc_counters_increment_received_IPIP(self):
		with self.lock:
			self.Received_Counter_IPIP += 1

	def merc_counters_increment_received_TP(self):
		with self.lock:
			self.Received_Counter_TP += 1

	def merc_counters_increment_received_PIM(self):
		with self.lock:
			self.Received_Counter_PIM += 1

	def merc_counters_increment_received_IPV6(self):
		with self.lock:
			self.Received_Counter_IPV6 += 1

	def merc_counters_increment_received_ROUTING(self):
		with self.lock:
			self.Received_Counter_ROUTING += 1

	def merc_counters_increment_received_FRAGMENT(self):
		with self.lock:
			self.Received_Counter_FRAGMENT += 1

	def merc_counters_increment_processed_HOPOPTS(self):
		with self.lock:
			self.Processed_Counter_HOPOPTS += 1

	def merc_counters_increment_processed_IP(self):
		with self.lock:
			self.Processed_Counter_IP += 1

	def merc_counters_increment_processed_ICMP(self):
		with self.Processed_Lock_ICMP:
			self.Processed_Counter_ICMP += 1

	def merc_counters_increment_processed_IGMP(self):
		with self.lock:
			self.Processed_Counter_IGMP += 1

	def merc_counters_increment_processed_SCTP(self):
		with self.lock:
			self.Processed_Counter_SCTP += 1

	def merc_counters_increment_processed_TCP(self):
		with self.Processed_Lock_TCP:
			self.Processed_Counter_TCP += 1

	def merc_counters_increment_processed_EGP(self):
		with self.lock:
			self.Processed_Counter_EGP += 1

	def merc_counters_increment_processed_PUP(self):
		with self.lock:
			self.Processed_Counter_PUP += 1

	def merc_counters_increment_processed_UDP(self):
		with self.Processed_Lock_UDP:
			self.Processed_Counter_UDP += 1

	def merc_counters_increment_processed_IDP(self):
		with self.lock:
			self.Processed_Counter_IDP += 1

	def merc_counters_increment_processed_IPIP(self):
		with self.lock:
			self.Processed_Counter_IPIP += 1

	def merc_counters_increment_processed_TP(self):
		with self.lock:
			self.Processed_Counter_TP += 1

	def merc_counters_increment_processed_PIM(self):
		with self.lock:
			self.Processed_Counter_PIM += 1

	def merc_counters_increment_processed_IPV6(self):
		with self.lock:
			self.Processed_Counter_IPV6 += 1

	def merc_counters_increment_processed_ROUTING(self):
		with self.lock:
			self.Processed_Counter_ROUTING += 1

	def merc_counters_increment_processed_FRAGMENT(self):
		with self.lock:
			self.Processed_Counter_FRAGMENT += 1

	# Get counters
	def merc_counters_get_received_HOPOPTS(self):
		with self.lock:
			return self.Received_Counter_HOPOPTS

	def merc_counters_get_received_IP(self):
		with self.lock:
			return self.Received_Counter_IP

	def merc_counters_get_received_ICMP(self):
		with self.lock:
			return self.Received_Counter_ICMP

	def merc_counters_get_received_IGMP(self):
		with self.lock:
			return self.Received_Counter_IGMP

	def merc_counters_get_received_SCTP(self):
		with self.lock:
			return self.Received_Counter_SCTP

	def merc_counters_get_received_TCP(self):
		with self.lock:
			return self.Received_Counter_TCP

	def merc_counters_get_received_EGP(self):
		with self.lock:
			return self.Received_Counter_EGP

	def merc_counters_get_received_PUP(self):
		with self.lock:
			return self.Received_Counter_PUP

	def merc_counters_get_received_UDP(self):
		with self.lock:
			return self.Received_Counter_UDP

	def merc_counters_get_received_IDP(self):
		with self.lock:
			return self.Received_Counter_IDP

	def merc_counters_get_received_IPIP(self):
		with self.lock:
			return self.Received_Counter_IPIP

	def merc_counters_get_received_TP(self):
		with self.lock:
			return self.Received_Counter_TP

	def merc_counters_get_received_PIM(self):
		with self.lock:
			return self.Received_Counter_PIM

	def merc_counters_get_received_IPV6(self):
		with self.lock:
			return self.Received_Counter_IPV6

	def merc_counters_get_received_ROUTING(self):
		with self.lock:
			return self.Received_Counter_ROUTING

	def merc_counters_get_received_FRAGMENT(self):
		with self.lock:
			return self.Received_Counter_FRAGMENT

	def merc_counters_get_received_RSVP(self):
		with self.lock:
			return self.Received_Counter_RSVP

	def merc_counters_get_processed_HOPOPTS(self):
		with self.lock:
			return self.Processed_Counter_HOPOPTS

	def merc_counters_get_processed_IP(self):
		with self.lock:
			return self.Processed_Counter_IP

	def merc_counters_get_processed_ICMP(self):
		with self.lock:
			return self.Processed_Counter_ICMP

	def merc_counters_get_processed_IGMP(self):
		with self.lock:
			return self.Processed_Counter_IGMP

	def merc_counters_get_processed_SCTP(self):
		with self.lock:
			return self.Processed_Counter_SCTP

	def merc_counters_get_processed_TCP(self):
		with self.lock:
			return self.Processed_Counter_TCP

	def merc_counters_get_processed_EGP(self):
		with self.lock:
			return self.Processed_Counter_EGP

	def merc_counters_get_processed_PUP(self):
		with self.lock:
			return self.Processed_Counter_PUP

	def merc_counters_get_processed_UDP(self):
		with self.lock:
			return self.Processed_Counter_UDP

	def merc_counters_get_processed_IDP(self):
		with self.lock:
			return self.Processed_Counter_IDP

	def merc_counters_get_processed_IPIP(self):
		with self.lock:
			return self.Processed_Counter_IPIP

	def merc_counters_get_processed_TP(self):
		with self.lock:
			return self.Processed_Counter_TP

	def merc_counters_get_processed_PIM(self):
		with self.lock:
			return self.Processed_Counter_PIM

	def merc_counters_get_processed_IPV6(self):
		with self.lock:
			return self.Processed_Counter_IPV6

	def merc_counters_get_processed_ROUTING(self):
		with self.lock:
			return self.Processed_Counter_ROUTING

	def merc_counters_get_processed_FRAGMENT(self):
		with self.lock:
			return self.Processed_Counter_FRAGMENT

	def merc_counters_get_processed_RSVP(self):
		with self.lock:
			return self.Processed_Counter_RSVP


