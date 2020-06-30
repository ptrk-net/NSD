# NSD_Network class

# Imports python libraries
import platform
import socket
import logging

# Import local libraries
from bin.NSD_Monitor import NSD_Monitor_Data
from bin.NSD_Packets_Queue import NSD_Packets_Queue
from conf import variables as vrb


class NSD_Network:

  # NSD_Init method
  def __init__(self, log_level, interface, sync_queue):
    self.log_level = log_level
    self.logger = logging.getLogger(__name__)
    self.iface = interface
    self.SQ = sync_queue

    self.logger.info('Opening socket..')
    try:
      if platform.system() == 'Linux':
        self.sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
        self.sock.bind((self.iface, 0))
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 2 ** 30)
      else:
        self.logger.error('NotImplementedError: platform not implemented yet')
        self.SQ.put('KILL')
    except PermissionError:
      self.logger.error('PermissionError: you must be root')
      self.SQ.put('KILL')
    except OSError:
      self.logger.error('OSError: sure the interface {} exists?'.format(self.iface))
      self.SQ.put('KILL')
    self.logger.info('Socket open!')

  # Listen to the network
  def receiver(self):
    self.logger.info('Ready to receive packets!')
    while True:
      try:
        packet = self.sock.recv(65565)
        prot = int.from_bytes(packet[23:24], byteorder='big')

        if prot == 6:
          NSD_Packets_Queue.insert_TCP_packet(packet)
          NSD_Monitor_Data.increment_total_received_TCP()
        elif prot == 17:
          NSD_Packets_Queue.insert_UDP_packet(packet)
          NSD_Monitor_Data.increment_total_received_UDP()
        elif prot == 2:
          NSD_Packets_Queue.insert_ICMP_packet(packet)
          NSD_Monitor_Data.increment_total_received_ICMP()
        else:
          NSD_Monitor_Data.increment_total_received_ERROR()
      except KeyboardInterrupt:
        if self.log_level >= vrb.INFO:
          self.logger.info('Closing sockets...')
        return
