# Network class

# Imports python libraries
import platform
import socket
import logging


# Class to process network packets
class NSD_Network:

    # Init method
    def __init__(self, interface, counters, pkts_queue, sync_queue, protocols_file):
        self.logger = logging.getLogger(__name__)
        self.iface = interface
        self.Counters = counters
        self.PQ = pkts_queue
        self.SQ = sync_queue
        self.Protocols_Table = dict()
        # self.Protocols_Table = {num:[name[8:],0] for name,num in vars(socket).items() if name.startswith("IPPROTO")}

        self.logger.info('Reading protocols..')
        try:
            prot_file = open(protocols_file, 'r')
            for line in prot_file.readlines():
                values = line.split(':')
                self.Protocols_Table[int(values[0])] = values[2]
            prot_file.close()
        except IOError as e:
            raise IOError('I/O error: ' + str(e.errno) + str(e.strerror))

        # self.Protocols_Table = {num:name[8:] for name,num in vars(socket).items() if name.startswith("IPPROTO")}
        # i=0
        # while i < len(self.Protocols_Table):
        #	self.logger.info('Protocol: ' + str(i) + ' -> ' + str(self.Protocols_Table[i]))
        #	i += 1

        self.logger.info('Opening socket..')
        try:
            if platform.system() == 'Linux':
                self.sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
                self.sock.bind((self.iface, 0))
                self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 2 ** 30)
            else:
                raise NotImplementedError('No implemented yet')
        except socket.error as msg:
            self.logger.error("Socket could not be created.\nError: {0} - {1}".format(str(msg[0]), str(msg[1])))
            self.SQ.put('KILL')

    # Listen to the network
    def NSD_Network_rcv(self):
        self.logger.info('Ready to receive packets!')
        while True:
            try:
                packet = self.sock.recv(65565)
                prot = int.from_bytes(packet[23:24], byteorder='big')
                # self.logger.info('Protocol: ' + str(prot) + ' --> ' + self.Protocols_Table[prot])
                getattr(self.PQ, 'NSD_Packets_queue_insert_' + self.Protocols_Table[prot])(packet)
                getattr(self.Counters, 'NSD_Counters_increment_received_' + self.Protocols_Table[prot])()
            except AttributeError as msg:
                self.logger.error('Not Implemented Error: ' + str(msg))
            except NotImplementedError as msg:
                self.logger.error('Not Implemented Error: ' + str(msg))
                self.SQ.put('KILL')
            except KeyError as msg:
                self.logger.error('No protocol found: ' + str(prot) + '--> ' + str(packet))
            # self.logger.info(packet)
            except KeyboardInterrupt:
                self.logger.error('Closing socket..')
                self.sock.close()
    # self.NSD_Network_process_packet(packet)

# Get packet counter for a protocol
# def NSD_Network_packet_counter(self, protocol):
#	return self.Protocols_Table[socket.getprotobyname(protocol)][1]
