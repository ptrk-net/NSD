# import system libraries
import platform
import socket


# Class to process network packets
class Merc_Network:

    # Init method
    def __init__(self, interface, counters, pkts_queue, sync_queue):
        self.iface = interface
        self.Counters = counters
        self.PQ = pkts_queue
        self.SQ = sync_queue
        self.Protocols_Table = dict()
        # self.Protocols_Table = {num:[name[8:],0] for name,num in vars(socket).items() if name.startswith("IPPROTO")}

        try:
            prot_file = open('Protocols', 'r')
        except IOError as e:
            print('I/O error: ' + str(e.errno) + str(e.strerror))
            return
        # self.Protocols_Table = {int(values[0]):values[2] for values in prot_file.readline().split(':')}
        try:
            for line in prot_file.readlines():
                values = line.split(':')
                self.Protocols_Table[int(values[0])] = values[2]
        finally:
            prot_file.close()

        # self.Protocols_Table = {num:name[8:] for name,num in vars(socket).items() if name.startswith("IPPROTO")}
        # i=0
        # while i < len(self.Protocols_Table):
        #	print('Protocol: ' + str(i) + ' -> ' + str(self.Protocols_Table[i]))
        #	i += 1

        try:
            if platform.system() == 'Linux':
                self.sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
                self.sock.bind((self.iface, 0))
                self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 2 ** 30)
            else:
                print('No implemented yet')
        except socket.error as msg:
            print("Socket could not be created.\nError: {0} - {1}".format(str(msg[0]), str(msg[1])))
            self.SQ.put('KILL')

    # Listen to the network
    def merc_network_rcv(self):
        while True:
            try:
                packet = self.sock.recv(65565)
                prot = int.from_bytes(packet[23:24], byteorder='big')

                # print('Protocol: ' + str(prot) + ' --> ' + self.Protocols_Table[prot])

                getattr(self.PQ, 'merc_packets_queue_insert_' + self.Protocols_Table[prot])(packet)
                getattr(self.Counters, 'merc_counters_increment_received_' + self.Protocols_Table[prot])()
            except AttributeError as msg:
                print('Not Implemented Error: ' + str(msg))
            except NotImplementedError as msg:
                print('Not Implemented Error: ' + str(msg))
                self.SQ.put('KILL')
            except KeyError as msg:
                print('No protocol found: ' + str(prot) + '--> ' + str(packet))
            # print(packet)
            except KeyboardInterrupt:
                print('Closing socket..')
                self.sock.close()
    # self.merc_network_process_packet(packet)

# Get packet counter for a protocol
# def merc_network_packet_counter(self, protocol):
#	return self.Protocols_Table[socket.getprotobyname(protocol)][1]
