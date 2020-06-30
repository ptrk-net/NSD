# Class to add the packet to the processing queue

# Imports python libraries
from multiprocessing import Manager


# Class to process protocols-based queues
class Packets_Queue:
  __manager = Manager()

  TCP_Queue = __manager.Queue()
  UDP_Queue = __manager.Queue()
  ICMP_Queue = __manager.Queue()
  RTP_PDU_Groups_Queue = __manager.Queue()

  @staticmethod
  def Packets_Queue_insert_TCP(packet):
    Packets_Queue.TCP_Queue.put(packet)

  @staticmethod
  def Packets_Queue_insert_UDP(packet):
    Packets_Queue.UDP_Queue.put(packet)

  @staticmethod
  def Packets_Queue_insert_ICMP(packet):
    Packets_Queue.ICMP_Queue.put(packet)

  @staticmethod
  def Packets_Queue_insert_RTP_Group_Features(group):
    Packets_Queue.RTP_PDU_Groups_Queue.put(group)

  @staticmethod
  def Packets_Queue_get_TCP():
    return Packets_Queue.TCP_Queue.get()

  @staticmethod
  def Packets_Queue_get_UDP():
    return Packets_Queue.UDP_Queue.get()

  @staticmethod
  def Packets_Queue_get_ICMP():
    return Packets_Queue.ICMP_Queue.get()

  @staticmethod
  def Packets_Queue_get_RTP_PDU_Groups():
    return Packets_Queue.RTP_PDU_Groups_Queue.get()

  @staticmethod
  def Packets_Queue_empty():
    return True if Packets_Queue.TCP_Queue.empty() and Packets_Queue.UDP_Queue.empty() and Packets_Queue.ICMP_Queue.empty() else False
