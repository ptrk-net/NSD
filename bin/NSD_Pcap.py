# Pcap reading class

# Imports python libraries
import dpkt
import logging

# Import NSD libraries
from bin.NSD_Monitor_Data import NSD_Monitor_Data


# Class to read pcaps file
class NSD_Pcap:

    # Init method
    def __init__(self, log_level, pcap_file, pkts_queue, sync_queue, protocols_file):
        self.log_level = log_level
        self.logger = logging.getLogger(__name__)
        self.PQ = pkts_queue
        self.SQ = sync_queue
        self.Protocols_Table = dict()

        self.logger.info('Reading pcap file: ' + pcap_file)
        try:
            self.file = dpkt.pcap.Reader(open(pcap_file, 'rb'))
        except ValueError as e:
            self.logger.error('Error reading the pcap file {0}: {1}'.format(pcap_file,str(e)))
            self.SQ.put('KILL')
            return None
        self.logger.info('PCAP file parsed!')

        self.logger.info('Reading protocols..')
        try:
            prot_file = open(protocols_file, 'r')
            for line in prot_file.readlines():
                values = line.split(':')
                self.Protocols_Table[int(values[0])] = values[2]
            prot_file.close()
        except IOError as e:
            raise IOError('I/O error: ' + str(e.errno) + str(e.strerror))
        self.logger.info('Protocols parsed!')

    # Process packets
    def NSD_Pcap_process(self):
        for ts, pkt in self.file:
            try:
                prot = int.from_bytes(pkt[23:24], byteorder='big')
                getattr(self.PQ, 'NSD_Packets_Queue_insert_' + self.Protocols_Table[prot])(pkt)
                getattr(NSD_Monitor_Data(),
                        'NSD_Monitor_Data_increment_total_received_' + self.Protocols_Table[prot])()
            except AttributeError as msg:
                self.logger.error('Not Implemented Error: ' + str(msg))
            except NotImplementedError as msg:
                self.logger.error('Not Implemented Error: ' + str(msg))
                # self.SQ.put('KILL')
            except KeyError as msg:
                self.logger.error('No protocol found: ' + str(prot) + '--> ' + str(pkt))
            except KeyboardInterrupt:
                self.logger.error('Closing socket..')

        self.SQ.put('PCAP_FINISHED')
        #exit(0)
