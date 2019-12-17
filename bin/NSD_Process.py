# Class to process the packets

# Import python libraries
import socket
import logging

# Import NSD libraries
from bin.NSD_Database import NSD_Database


# Class to make the first packets classification based in the protocol
class NSD_Process:

    def __init__(self, log_level, db_server, db_port, counters, sync_queue):
        self.log_level = log_level
        self.logger = logging.getLogger(__name__)
        self.Counters = counters
        self.SQ = sync_queue
        self.db_server = db_server
        self.db_port = db_port

    def NSD_Process_fork_database(self):
        self.DB = NSD_Database(self.log_level, self.db_server, self.db_port, self.SQ)  # MongoDB

    # Process Live packets
    def NSD_Process_live_ICMP(self, queue):
        self.NSD_Process_fork_database()
        while True:
            try:
                packet = queue.get()

                Source_IP = socket.inet_ntoa(packet[26:30])
                Dest_IP = socket.inet_ntoa(packet[30:34])
                Type = int.from_bytes(packet[34:35], byteorder='big')
                Code = int.from_bytes(packet[35:36], byteorder='big')
                Checksum = int.from_bytes(packet[36:38], byteorder='big')
                Header = int.from_bytes(packet[38:42], byteorder='big')
                Payload = int.from_bytes(packet[42:50], byteorder='big')

                self.DB.NSD_Database_insert_ICMP_packet([Source_IP, Dest_IP, Type, Code, Checksum, Header, Payload])

                self.Counters.NSD_Counters_increment_total_database_ICMP()
            except KeyboardInterrupt:
                print('Closing ICMP process..')
                return

    def NSD_Process_live_TCP(self, queue):
        self.NSD_Process_fork_database()
        while True:
            try:
                packet = queue.get()

                Source_IP = socket.inet_ntoa(packet[26:30])
                Dest_IP = socket.inet_ntoa(packet[30:34])
                Source_Port = int.from_bytes(packet[34:36], byteorder='big')
                Dest_Port = int.from_bytes(packet[36:38], byteorder='big')
                Sequence_Number = int.from_bytes(packet[38:42], byteorder='big')
                ACK_Number = int.from_bytes(packet[42:46], byteorder='big')
                Flags = int.from_bytes(packet[46:48], byteorder='big')
                Window = int.from_bytes(packet[48:50], byteorder='big')
                Checksum = int.from_bytes(packet[50:52], byteorder='big')
                Urgent_Pointer = int.from_bytes(packet[52:54], byteorder='big')
                Data = packet[54:].decode('unicode_escape').encode('utf-8')

                # print([Source_IP, Dest_IP, Source_Port, Dest_Port, Sequence_Number, ACK_Number, Data])
                self.DB.NSD_Database_insert_TCP_packet([Source_IP, Dest_IP, Source_Port, Dest_Port, Sequence_Number,
                                                        ACK_Number, Flags, Window, Checksum, Urgent_Pointer, Data])

                self.Counters.NSD_Counters_increment_total_database_TCP()
            except UnicodeDecodeError as msg:
                print('TCP Codec Error: ' + str(msg))
            except KeyboardInterrupt:
                print('Closing TCP process..')
                return

    def NSD_Process_live_UDP(self, queue):
        self.NSD_Process_fork_database()
        while True:
            try:
                packet = queue.get()

                Source_IP = socket.inet_ntoa(packet[26:30])
                Dest_IP = socket.inet_ntoa(packet[30:34])
                Source_Port = int.from_bytes(packet[34:36], byteorder='big')
                Dest_Port = int.from_bytes(packet[36:38], byteorder='big')
                Length = int.from_bytes(packet[38:40], byteorder='big')
                Checksum = int.from_bytes(packet[40:42], byteorder='big')
                Data = packet[42:].decode('unicode_escape').encode('utf-8')

                # print([Date, Source_IP, Dest_IP, Source_Port, Dest_Port, Data])
                self.DB.NSD_Database_insert_UDP_packet([Source_IP, Dest_IP, Source_Port, Dest_Port,
                                                        Length, Checksum, Data])

                self.Counters.NSD_Counters_increment_total_database_UDP()
            except UnicodeDecodeError as msg:
                print('UDP Codec Error: ' + str(msg))
            except KeyboardInterrupt:
                print('Closing UDP process..')
                return

    def NSD_Process_live_HOPOPTS(self, queue):
        raise NotImplementedError('developing HOPOPTS..')

    def NSD_Process_live_IP(self, queue):
        raise NotImplementedError('developing IP..')

    def NSD_Process_live_IGMP(self, queue):
        raise NotImplementedError('developing IGMP..')

    def NSD_Process_live_SCTP(self, queue):
        raise NotImplementedError('developing SCTP..')

    def NSD_Process_live_EGP(self, queue, counter):
        raise NotImplementedError('developing EGP..')

    def NSD_Process_live_PUP(self, queue):
        raise NotImplementedError('developing PUP..')

    def NSD_Process_live_IDP(self, queue):
        raise NotImplementedError('developing IDP..')

    def NSD_Process_live_IPIP(self, queue):
        raise NotImplementedError('developing IPIP..')

    def NSD_Process_live_TP(self, queue):
        raise NotImplementedError('developing TP..')

    def NSD_Process_live_PIM(self, queue):
        raise NotImplementedError('developing PIM..')

    def NSD_Process_live_IPV6(self, queue):
        raise NotImplementedError('developing IPV6..')

    def NSD_Process_live_ROUTING(self, queue):
        raise NotImplementedError('developing ROUTING..')

    def NSD_Process_live_FRAGMENT(self, queue):
        raise NotImplementedError('developing FRAGMENT..')

    def NSD_Process_live_RSVP(self, queue):
        raise NotImplementedError('developing RSVP..')

    def NSD_Process_live_GRE(self, queue):
        raise NotImplementedError('developing GRE..')

    def NSD_Process_live_ESP(self, queue):
        raise NotImplementedError('developing ESP..')

    def NSD_Process_live_AH(self, queue):
        raise NotImplementedError('developing AH..')

    def NSD_Process_live_ICMPV6(self, queue):
        raise NotImplementedError('developing ICMPV6..')

    def NSD_Process_live_NONE(self, queue):
        raise NotImplementedError('developing NONE..')

    def NSD_Process_live_DSTOPTS(self, queue):
        raise NotImplementedError('developing DSTOPTS..')

    def NSD_Process_live_RAW(self, queue):
        raise NotImplementedError('developing RAW..')
