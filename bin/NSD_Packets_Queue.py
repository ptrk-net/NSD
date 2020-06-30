# Class to add the packet to the processing queue

# Imports python libraries
from multiprocessing import Manager


# Class to process protocols-based queues
class NSD_Packets_Queue:
  __manager = Manager()

  TCP_Queue = __manager.Queue()
  UDP_Queue = __manager.Queue()
  ICMP_Queue = __manager.Queue()
  RTP_PDU_Groups_Queue = __manager.Queue()

  @staticmethod
  def insert_TCP_packet(packet):
    NSD_Packets_Queue.TCP_Queue.put(packet)

  @staticmethod
  def insert_UDP_packet(packet):
    NSD_Packets_Queue.UDP_Queue.put(packet)

  @staticmethod
  def insert_ICMP_packet(packet):
    NSD_Packets_Queue.ICMP_Queue.put(packet)

  @staticmethod
  def insert_RTP_Group_Features(group):
    NSD_Packets_Queue.RTP_PDU_Groups_Queue.put(group)

  @staticmethod
  def get_TCP_packet():
    return NSD_Packets_Queue.TCP_Queue.get()

  @staticmethod
  def get_UDP_packet():
    return NSD_Packets_Queue.UDP_Queue.get()

  @staticmethod
  def get_ICMP_packet():
    return NSD_Packets_Queue.ICMP_Queue.get()

  @staticmethod
  def get_RTP_PDU_Groups():
    return NSD_Packets_Queue.RTP_PDU_Groups_Queue.get()

  @staticmethod
  def empty():
    return True if NSD_Packets_Queue.TCP_Queue.empty() and NSD_Packets_Queue.UDP_Queue.empty() and NSD_Packets_Queue.ICMP_Queue.empty() else False
