# import system libraries
import socket
import unicodedata


# import Merc libraries
#from merc_packets_queue import Merc_Packets_Queue
from merc_database import Merc_Database

# Class to make the first packets classification based in the protocol
class Merc_Process:

	def __init__(self, counters, db, sync_queue):
		self.Counters = counters
		self.DB = db
		self.SQ = sync_queue

	# Process Live packets
	def merc_process_live_HOPOPTS(self, queue):
		raise NotImplementedError('developing HOPOPTS..')

	def merc_process_live_IP(self, queue):
		raise NotImplementedError('developing IP..')

	def merc_process_live_ICMP(self, queue):
		while True:
			try:
				packet = queue.get()

				Source_IP = socket.inet_ntoa(packet[26:30])
				Dest_IP = socket.inet_ntoa(packet[30:34])
				Type = int.from_bytes(packet[34:35], byteorder='big')
				Code = int.from_bytes(packet[35:36], byteorder='big')

				#print([Date, Source_IP, Dest_IP, Type, Code])
				self.DB.merc_database_insert_ICMP_packet_inMemory([Source_IP, Dest_IP, Type, Code])

				self.Counters.merc_counters_increment_processed_ICMP()
			except KeyboardInterrupt:
				print('Closing ICMP process..')
				return


	def merc_process_live_IGMP(self, queue):
		raise NotImplementedError('developing IGMP..')

	def merc_process_live_SCTP(self, queue):
		raise NotImplementedError('developing SCTP..')

	def merc_process_live_TCP(self, queue):
		while True:
			try:
				packet = queue.get()

				Source_IP = socket.inet_ntoa(packet[26:30])
				Dest_IP = socket.inet_ntoa(packet[30:34])
				Source_Port = int.from_bytes(packet[34:36], byteorder='big')
				Dest_Port =  int.from_bytes(packet[36:38], byteorder='big')
				Sequence_Number = int.from_bytes(packet[38:42], byteorder='big')
				ACK_Number = int.from_bytes(packet[42:46], byteorder='big')
				Data = packet[54:].decode('unicode_escape').encode('utf-8')
		
				#print([Source_IP, Dest_IP, Source_Port, Dest_Port, Sequence_Number, ACK_Number, Data])
				self.DB.merc_database_insert_TCP_packet_inMemory([Source_IP, Dest_IP, Source_Port, Dest_Port, Sequence_Number, ACK_Number, Data])

				self.Counters.merc_counters_increment_processed_TCP()
			except UnicodeDecodeError as msg:
				print('TCP Codec Error: ' + str(msg))
			except KeyboardInterrupt:
				print('Closing TCP process..')
				return
		

	def merc_process_live_EGP(self, queue, counter):
		raise NotImplementedError('developing EGP..')

	def merc_process_live_PUP(self, queue):
		raise NotImplementedError('developing PUP..')

	def merc_process_live_UDP(self, queue):
		while True:
			try:
				packet = queue.get()

				Source_IP = socket.inet_ntoa(packet[26:30])
				Dest_IP = socket.inet_ntoa(packet[30:34])
				Source_Port = int.from_bytes(packet[34:36], byteorder='big')
				Dest_Port =  int.from_bytes(packet[36:38], byteorder='big')
				Data = packet[42:].decode('unicode_escape').encode('utf-8')

				#print([Date, Source_IP, Dest_IP, Source_Port, Dest_Port, Data])
				self.DB.merc_database_insert_UDP_packet_inMemory([Source_IP, Dest_IP, Source_Port, Dest_Port, Data])

				self.Counters.merc_counters_increment_processed_UDP()
			except UnicodeDecodeError as msg:
				print('UDP Codec Error: ' + str(msg))
			except KeyboardInterrupt:
				print('Closing UDP process..')
				return


	def merc_process_live_IDP(self, queue):
		raise NotImplementedError('developing IDP..')

	def merc_process_live_IPIP(self, queue):
		raise NotImplementedError('developing IPIP..')

	def merc_process_live_TP(self, queue):
		raise NotImplementedError('developing TP..')

	def merc_process_live_PIM(self, queue):
		raise NotImplementedError('developing PIM..')

	def merc_process_live_IPV6(self, queue):
		raise NotImplementedError('developing IPV6..')

	def merc_process_live_ROUTING(self, queue):
		raise NotImplementedError('developing ROUTING..')

	def merc_process_live_FRAGMENT(self, queue):
		raise NotImplementedError('developing FRAGMENT..')

	def merc_process_live_RSVP(self, queue):
		raise NotImplementedError('developing RSVP..')

	def merc_process_live_GRE(self, queue):
		raise NotImplementedError('developing GRE..')

	def merc_process_live_ESP(self, queue):
		raise NotImplementedError('developing ESP..')

	def merc_process_live_AH(self, queue):
		raise NotImplementedError('developing AH..')

	def merc_process_live_ICMPV6(self, queue):
		raise NotImplementedError('developing ICMPV6..')

	def merc_process_live_NONE(self, queue):
		raise NotImplementedError('developing NONE..')

	def merc_process_live_DSTOPTS(self, queue):
		raise NotImplementedError('developing DSTOPTS..')

	def merc_process_live_RAW(self, queue):
		raise NotImplementedError('developing RAW..')


	# Process conversations
	def merc_process_conversation_HOPOPTS(self, queue):
		raise NotImplementedError('developing HOPOPTS..')

	def merc_process_conversation_IP(self, queue):
		raise NotImplementedError('developing IP..')

	def merc_process_conversation_ICMP(self, queue):
		while True:
			try:
				packet = queue.get()

				Source_IP = socket.inet_ntoa(packet[26:30])
				Dest_IP = socket.inet_ntoa(packet[30:34])
				Type = int.from_bytes(packet[34:35], byteorder='big')
				Code = int.from_bytes(packet[35:36], byteorder='big')

				#print([Date, Source_IP, Dest_IP, Type, Code])
				self.DB.merc_database_insert_ICMP_packet_inMemory([Source_IP, Dest_IP, Type, Code])

				self.Counters.merc_counters_increment_processed_ICMP()
			except KeyboardInterrupt:
				print('Closing ICMP process..')
				return


	def merc_process_conversation_IGMP(self, queue):
		raise NotImplementedError('developing IGMP..')

	def merc_process_conversation_SCTP(self, queue):
		raise NotImplementedError('developing SCTP..')

	def merc_process_conversation_TCP(self, queue):
		while True:
			try:
				select = "SELECT Source_IP, Dest_IP, Source_Port, Dest_Port, MAX(Sequence_Number), MAX(ACK_Number) FROM TCP GROUP BY Source_IP, Dest_IP, Source_Port, Dest_Port"
				delete = "DELETE FROM TCP WHERE "
				with self.DB.merc_database_get_lock():
					print('aaa')
			except KeyboardInterrupt:
				print('Closing TCP process..')
				return
		

	def merc_process_conversation_EGP(self, queue, counter):
		raise NotImplementedError('developing EGP..')

	def merc_process_conversation_PUP(self, queue):
		raise NotImplementedError('developing PUP..')

	def merc_process_conversation_UDP(self, queue):
		while True:
			try:
				packet = queue.get()

				Source_IP = socket.inet_ntoa(packet[26:30])
				Dest_IP = socket.inet_ntoa(packet[30:34])
				Source_Port = int.from_bytes(packet[34:36], byteorder='big')
				Dest_Port =  int.from_bytes(packet[36:38], byteorder='big')
				Data = str(packet[42:])

				#print([Date, Source_IP, Dest_IP, Source_Port, Dest_Port, Data])
				self.DB.merc_database_insert_UDP_packet_inMemory([Source_IP, Dest_IP, Source_Port, Dest_Port, Data])

				self.Counters.merc_counters_increment_processed_UDP()
			except KeyboardInterrupt:
				print('Closing UDP process..')
				return


	def merc_process_conversation_IDP(self, queue):
		raise NotImplementedError('developing IDP..')

	def merc_process_conversation_IPIP(self, queue):
		raise NotImplementedError('developing IPIP..')

	def merc_process_conversation_TP(self, queue):
		raise NotImplementedError('developing TP..')

	def merc_process_conversation_PIM(self, queue):
		raise NotImplementedError('developing PIM..')

	def merc_process_conversation_IPV6(self, queue):
		raise NotImplementedError('developing IPV6..')

	def merc_process_conversation_ROUTING(self, queue):
		raise NotImplementedError('developing ROUTING..')

	def merc_process_conversation_FRAGMENT(self, queue):
		raise NotImplementedError('developing FRAGMENT..')

	def merc_process_conversation_RSVP(self, queue):
		raise NotImplementedError('developing RSVP..')

	def merc_process_conversation_GRE(self, queue):
		raise NotImplementedError('developing GRE..')

	def merc_process_conversation_ESP(self, queue):
		raise NotImplementedError('developing ESP..')

	def merc_process_conversation_AH(self, queue):
		raise NotImplementedError('developing AH..')

	def merc_process_conversation_ICMPV6(self, queue):
		raise NotImplementedError('developing ICMPV6..')

	def merc_process_conversation_NONE(self, queue):
		raise NotImplementedError('developing NONE..')

	def merc_process_conversation_DSTOPTS(self, queue):
		raise NotImplementedError('developing DSTOPTS..')

	def merc_process_conversation_RAW(self, queue):
		raise NotImplementedError('developing RAW..')

