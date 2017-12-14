# import system libraries
import platform, socket

#import Merc libraries

# Class to process network packets
class Merc_Network:

	# Init method
	def __init__(self, interface, counters, pkts_queue, sync_queue):
		self.iface = interface
		#self.Protocols_Table = {num:[name[8:],0] for name,num in vars(socket).items() if name.startswith("IPPROTO")}
		self.Protocols_Table = {num:name[8:] for name,num in vars(socket).items() if name.startswith("IPPROTO")}
		self.Counters = counters
		self.PQ = pkts_queue
		self.SQ = sync_queue

		try:
			if platform.system() == 'Linux' :
				self.sock = socket.socket( socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003) )
				self.sock.bind( (self.iface,0) )
				self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 2**30)
			else:
				print( 'No implemented yet' )
		except socket.error as msg:
			print('Socket could not be created.\nError: ' + str(msg[0]) + ' - ' + str(msg[1]))
			self.SQ.put('KILL')

	# Listen to the network
	def merc_network_rcv(self):
		while True:
			try:
				packet = self.sock.recv(65565)
				prot = int.from_bytes(packet[23:24], byteorder='big')

				#print('Protocol: ' + self.Protocols_Table[prot][0] + ' --> ' + str(self.Protocols_Table[prot][1]))

				getattr(self.PQ, 'merc_packets_queue_insert_' + self.Protocols_Table[prot])(packet)
				getattr(self.Counters, 'merc_counters_increment_received_' + self.Protocols_Table[prot])()
				counter.merddc_counter_increment()
			except NotImplementedError as msg:
				print('ERROR: ' + str(msg))
				self.SQ.put('KILL')
			except KeyError as msg:
				print('No protocol found: ' + str(msg))
				#print(packet)
			except KeyboardInterrupt:
				print('Closing socket..')
				self.sock.close()
		#self.merc_network_process_packet(packet)

	# Get packet counter for a protocol
	#def merc_network_packet_counter(self, protocol):
	#	return self.Protocols_Table[socket.getprotobyname(protocol)][1]

