# Pcap reading class

# Imports python libraries
import dpkt
import logging

# Import local libraries
from bin.Monitor import Monitor_Data
from bin.Packets_Queue import Packets_Queue
from conf import variables as vrb


# Class to read pcaps file
class Pcap:

  # Init method
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
  def Pcap_process(self):
    self.logger.info('Getting packets from file...')
    for ts, pkt in self.file:
      prot = int.from_bytes(pkt[23:24], byteorder='big')

      if prot == 6:
        Packets_Queue.Packets_Queue_insert_TCP(pkt)
        Monitor_Data.Monitor_Data_increment_total_received_TCP()
      elif prot == 17:
        Packets_Queue.Packets_Queue_insert_UDP(pkt)
        Monitor_Data.Monitor_Data_increment_total_received_UDP()
      elif prot == 2:
        Packets_Queue.Packets_Queue_insert_ICMP(pkt)
        Monitor_Data.Monitor_Data_increment_total_received_ICMP()
      else:
        Monitor_Data.Monitor_Data_increment_total_received_ERROR()

    self.logger.info('All packets readed!')
    self.SQ.put('PCAP_FINISHED')
    if not self.set_analyze:
      self.SQ.put('KILL')
