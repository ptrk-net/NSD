# import system libraries
from multiprocessing import Queue

# Class to process protocols-based queues
class Merc_Packets_Queue:

	# Merc 
	def __init__(self):
		self.TCP_Queue = Queue()
		self.UDP_Queue = Queue()
		self.ICMP_Queue = Queue()
 
	# Process
	def merc_packets_queue_insert_HOPOPT(self, packet):
		raise NotImplementedError('developing HOPOPT..')

	def merc_packets_queue_insert_IP(self, packet):
		raise NotImplementedError('developing IP..')

	def merc_packets_queue_insert_ICMP(self, packet):
		self.ICMP_Queue.put(packet)

	def merc_packets_queue_insert_IGMP(self, packet):
		raise NotImplementedError('developing IGMP..')

	def merc_packets_queue_insert_SCTP(self, packet):
		raise NotImplementedError('developing SCTP..')

	def merc_packets_queue_insert_TCP(self, packet):
		self.TCP_Queue.put(packet)

	def merc_packets_queue_insert_EGP(self, packet):
		raise NotImplementedError('developing EGP..')

	def merc_packets_queue_insert_PUP(self, packet):
		raise NotImplementedError('developing PUP..')

	def merc_packets_queue_insert_UDP(self, packet):
		self.UDP_Queue.put(packet)

	def merc_packets_queue_insert_IDP(self, packet):
		raise NotImplementedError('developing IDP..')

	def merc_packets_queue_insert_IPIP(self, packet):
		raise NotImplementedError('developing IPIP..')

	def merc_packets_queue_insert_TP(self, packet):
		raise NotImplementedError('developing TP..')

	def merc_packets_queue_insert_PIM(self, packet):
		raise NotImplementedError('developing PIM..')

	def merc_packets_queue_insert_IPV6(self, packet):
		raise NotImplementedError('developing IPV6..')

	def merc_packets_queue_insert_ROUTING(self, packet):
		raise NotImplementedError('developing ROUTING..')

	def merc_packets_queue_insert_FRAGMENT(self, packet):
		raise NotImplementedError('developing FRAGMENT..')

	def merc_packets_queue_insert_RSVP(self, packet):
		raise NotImplementedError('developing RSVP..')

	def merc_packets_queue_insert_GRE(self, packet):
		raise NotImplementedError('developing GRE..')

	def merc_packets_queue_insert_ESP(self, packet):
		raise NotImplementedError('developing ESP..')

	def merc_packets_queue_insert_AH(self, packet):
		raise NotImplementedError('developing AH..')

	def merc_packets_queue_insert_ICMPV6(self, packet):
		raise NotImplementedError('developing ICMPV6..')

	def merc_packets_queue_insert_NONE(self, packet):
		raise NotImplementedError('developing NONE..')

	def merc_packets_queue_insert_DSTOPTS(self, packet):
		raise NotImplementedError('developing DSTOPTS..')

	def merc_packets_queue_insert_RAW(self, packet):
		raise NotImplementedError('developing RAW..')

