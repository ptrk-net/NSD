# import system libraries
import socket
from datetime import datetime

# import Merc libraries
#from merc_packets_queue import Merc_Packets_Queue
from merc_database import Merc_Database

# Class to make the first packets classification based in the protocol
class Merc_Processing:

	def __init__(self, counters, db, sync_queue):
		self.Counters = counters
		self.DB = db
		self.SQ = sync_queue

	# Process
	def merc_processing_HOPOPTS(self, queue):
		raise NotImplementedError('developing HOPOPTS..')

	def merc_processing_IP(self, queue):
		raise NotImplementedError('developing IP..')

	def merc_processing_ICMP(self, queue):
		while True:
			try:
				packet = queue.get()

				Date = datetime.now().strftime('%d/%m/%Y %H:%M:%S.%f')
				Source_IP = socket.inet_ntoa(packet[26:30])
				Dest_IP = socket.inet_ntoa(packet[30:34])
				Type = int.from_bytes(packet[34:35], byteorder='big')
				Code = int.from_bytes(packet[35:36], byteorder='big')

				#print([Date, Source_IP, Dest_IP, Type, Code])
				self.DB.merc_database_insert_ICMP_packet([Date, Source_IP, Dest_IP, Type, Code])

				self.Counters.merc_counters_increment_processed_ICMP()
			except KeyboardInterrupt:
				print('Closing ICMP process..')
				return


	def merc_processing_IGMP(self, queue):
		raise NotImplementedError('developing IGMP..')

	def merc_processing_SCTP(self, queue):
		raise NotImplementedError('developing SCTP..')

	def merc_processing_TCP(self, queue):
		while True:
			try:
				packet = queue.get()

				Date = datetime.now().strftime('%d/%m/%Y %H:%M:%S.%f')
				Source_IP = socket.inet_ntoa(packet[26:30])
				Dest_IP = socket.inet_ntoa(packet[30:34])
				Source_Port = int.from_bytes(packet[34:36], byteorder='big')
				Dest_Port =  int.from_bytes(packet[36:38], byteorder='big')
				Sequence_Number = int.from_bytes(packet[38:42], byteorder='big')
				ACK_Number = int.from_bytes(packet[42:46], byteorder='big')
				Data = str(packet[54:])
		
				#print([Date, Source_IP, Dest_IP, Source_Port, Dest_Port, Sequence_Number, ACK_Number, Data])
				self.DB.merc_database_insert_TCP_packet([Date, Source_IP, Dest_IP, Source_Port, Dest_Port, Sequence_Number, ACK_Number, Data])

				self.Counters.merc_counters_increment_processed_TCP()
			except KeyboardInterrupt:
				print('Closing TCP process..')
				return
		

	def merc_processing_EGP(self, queue, counter):
		raise NotImplementedError('developing EGP..')

	def merc_processing_PUP(self, queue):
		raise NotImplementedError('developing PUP..')

	def merc_processing_UDP(self, queue):
		while True:
			try:
				packet = queue.get()

				Date = datetime.now().strftime('%d/%m/%Y %H:%M:%S.%f')
				Source_IP = socket.inet_ntoa(packet[26:30])
				Dest_IP = socket.inet_ntoa(packet[30:34])
				Source_Port = int.from_bytes(packet[34:36], byteorder='big')
				Dest_Port =  int.from_bytes(packet[36:38], byteorder='big')
				Data = str(packet[42:])

				#print([Date, Source_IP, Dest_IP, Source_Port, Dest_Port, Data])
				self.DB.merc_database_insert_UDP_packet([Date, Source_IP, Dest_IP, Source_Port, Dest_Port, Data])

				self.Counters.merc_counters_increment_processed_UDP()
			except KeyboardInterrupt:
				print('Closing UDP process..')
				return


	def merc_processing_IDP(self, queue):
		raise NotImplementedError('developing IDP..')

	def merc_processing_IPIP(self, queue):
		raise NotImplementedError('developing IPIP..')

	def merc_processing_TP(self, queue):
		raise NotImplementedError('developing TP..')

	def merc_processing_PIM(self, queue):
		raise NotImplementedError('developing PIM..')

	def merc_processing_IPV6(self, queue):
		raise NotImplementedError('developing IPV6..')

	def merc_processing_ROUTING(self, queue):
		raise NotImplementedError('developing ROUTING..')

	def merc_processing_FRAGMENT(self, queue):
		raise NotImplementedError('developing FRAGMENT..')

	def merc_processing_RSVP(self, queue):
		raise NotImplementedError('developing RSVP..')

	def merc_processing_GRE(self, queue):
		raise NotImplementedError('developing GRE..')

	def merc_processing_ESP(self, queue):
		raise NotImplementedError('developing ESP..')

	def merc_processing_AH(self, queue):
		raise NotImplementedError('developing AH..')

	def merc_processing_ICMPV6(self, queue):
		raise NotImplementedError('developing ICMPV6..')

	def merc_processing_NONE(self, queue):
		raise NotImplementedError('developing NONE..')

	def merc_processing_DSTOPTS(self, queue):
		raise NotImplementedError('developing DSTOPTS..')

	def merc_processing_RAW(self, queue):
		raise NotImplementedError('developing RAW..')

