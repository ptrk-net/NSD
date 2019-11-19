# Pcap reading class

# Imports python libraries
import dpkt
import logging


# Class to read pcaps file
class NSD_Pcap:

    # Init method
    def __init__(self, pcap_file, counters, pkts_queue, sync_queue, protocols_file):
        self.logger = logging.getLogger(__name__)
        self.Counters = counters
        self.PQ = pkts_queue
        self.SQ = sync_queue
        self.Protocols_Table = dict()

        self.logger.info('Reading pcap..')
        try:
            self.file = dpkt.pcap.Reader(open(pcap_file, 'r'))
        finally:
            self.logger.error('Error reading the pcap file {0}'.format(pcap_file))

        self.logger.info('Reading protocols..')
        try:
            prot_file = open(protocols_file, 'r')
            for line in prot_file.readlines():
                values = line.split(':')
                self.Protocols_Table[int(values[0])] = values[2]
            prot_file.close()
        except IOError as e:
            raise IOError('I/O error: ' + str(e.errno) + str(e.strerror))

    # Process packets
    def NSD_Pcap_process(self):
        for ts, pkt in self.file:
            try:
                prot = int.from_bytes(pkt[23:24], byteorder='big')
                getattr(self.PQ, 'NSD_Packets_queue_insert_' + self.Protocols_Table[prot])(pkt)
                getattr(self.Counters, 'NSD_Counters_increment_received_' + self.Protocols_Table[prot])()
            except AttributeError as msg:
                self.logger.error('Not Implemented Error: ' + str(msg))
            except NotImplementedError as msg:
                self.logger.error('Not Implemented Error: ' + str(msg))
                self.SQ.put('KILL')
            except KeyError as msg:
                self.logger.error('No protocol found: ' + str(prot) + '--> ' + str(pkt))
            except KeyboardInterrupt:
                self.logger.error('Closing socket..')

