# NSD_Pcap reading class

# Imports python libraries
import dpkt
import logging

# Import local libraries
from bin.NSD_Monitor import NSD_Monitor_Data
from bin.NSD_Packets_Queue import NSD_Packets_Queue
from conf import variables as vrb


# Class to read pcaps file
class NSD_Pcap:

  # NSD_Init method
  def __init__(self, log_level, sync_queue, pcapfile):
    self.log_level = log_level
    self.logger = logging.getLogger(__name__)
    self.SQ = sync_queue
    self.set_analyze = True if len(pcapfile) == 1 else False

    if self.set_analyze:
      self.logger.info('Reading pcap file\'{}\' to analyze it'.format(pcapfile[0]))
    else:
      self.logger.info('Reading pcap file \'{}\' as \'{}\' traffic'.format(pcapfile[0], pcapfile[1]))
    try:
      self.file = dpkt.pcap.Reader(open(pcapfile[0], 'rb'))
    except ValueError as e:
      self.logger.error('Error reading the pcap file {}: {}'.format(pcapfile[0], str(e)))
      self.SQ.put('KILL')

    if self.log_level >= vrb.INFO:
      self.logger.info('PCAP file parsed!')

  # Process packets
  def process_pcapfile(self):
    self.logger.info('Getting packets from file...')
    for ts, pkt in self.file:
      prot = int.from_bytes(pkt[23:24], byteorder='big')

      if prot == 6:
        NSD_Packets_Queue.insert_TCP_packet(pkt)
        NSD_Monitor_Data.increment_total_received_TCP()
      elif prot == 17:
        NSD_Packets_Queue.insert_UDP_packet(pkt)
        NSD_Monitor_Data.increment_total_received_UDP()
      elif prot == 2:
        NSD_Packets_Queue.insert_ICMP_packet(pkt)
        NSD_Monitor_Data.increment_total_received_ICMP()
      else:
        NSD_Monitor_Data.increment_total_received_ERROR()

    self.logger.info('All packets readed!')
    self.SQ.put('PCAP_FINISHED')
    if not self.set_analyze:
      self.SQ.put('KILL')
