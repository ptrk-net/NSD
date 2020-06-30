# Class to process the packets

# Import python libraries
import socket
import logging

# Import local libraries
from bin.Database import Database
from bin.Monitor import Monitor_Data
from bin.Packets_Queue import Packets_Queue
from conf import variables as vrb


# Class to make the first packets classification based in the protocol
class Processor:

  def __init__(self, log_level, db_server, db_port, db_name, sync_queue, pcap_type=None):
    self.log_level = log_level
    self.logger = logging.getLogger(__name__)
    self.SQ = sync_queue
    self.db_server = db_server
    self.db_port = db_port
    self.db_name = db_name
    self.pcap_type = pcap_type

  def Processor_fork_database(self):
    self.DB = Database(self.log_level, self.db_server, self.db_port, self.db_name, self.SQ)

  # Process Live packets
  def Processor_live_ICMP(self):
    self.Processor_fork_database()
    while True:
      try:
        packet = Packets_Queue.Packets_Queue_get_UDP()

        Source_IP = socket.inet_ntoa(packet[26:30])
        Dest_IP = socket.inet_ntoa(packet[30:34])
        Type = int.from_bytes(packet[34:35], byteorder='big')
        Code = int.from_bytes(packet[35:36], byteorder='big')
        Checksum = int.from_bytes(packet[36:38], byteorder='big')
        Header = int.from_bytes(packet[38:42], byteorder='big')
        Payload = int.from_bytes(packet[42:50], byteorder='big')
        Traffic_CC = self.pcap_type

        self.DB.Database_insert_ICMP_packet([Source_IP, Dest_IP, Type, Code, Checksum, Header, Payload,
                                             Traffic_CC])

        Monitor_Data.Monitor_Data_increment_total_database_ICMP()
      except KeyboardInterrupt:
        if self.log_level >= vrb.INFO:
          self.logger.info('Closing ICMP process..')
        return

  def Processor_live_TCP(self):
    self.Processor_fork_database()
    while True:
      try:
        packet = Packets_Queue.Packets_Queue_get_TCP()

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
        Data = packet[54:]
        Traffic_CC = self.pcap_type

        self.DB.Database_insert_TCP_packet([Source_IP, Dest_IP, Source_Port, Dest_Port, Sequence_Number,
                                            ACK_Number, Flags, Window, Checksum, Urgent_Pointer, Data,
                                            Traffic_CC])

        Monitor_Data.Monitor_Data_increment_total_database_TCP()
      except KeyboardInterrupt:
        if self.log_level >= vrb.INFO:
          self.logger.info('Closing TCP process..')
        return

  def Processor_live_UDP(self):
    self.Processor_fork_database()
    while True:
      try:
        packet = Packets_Queue.Packets_Queue_get_UDP()

        Source_IP = socket.inet_ntoa(packet[26:30])
        Dest_IP = socket.inet_ntoa(packet[30:34])
        Source_Port = int.from_bytes(packet[34:36], byteorder='big')
        Dest_Port = int.from_bytes(packet[36:38], byteorder='big')
        Length = int.from_bytes(packet[38:40], byteorder='big')
        Checksum = int.from_bytes(packet[40:42], byteorder='big')
        UDP_type = int.from_bytes(packet[42:43], byteorder='big')
        Data = packet[42:]
        Traffic_CC = self.pcap_type

        self.DB.Database_insert_UDP_packet([Source_IP, Dest_IP, Source_Port, Dest_Port,
                                            Length, Checksum, UDP_type, Data, Traffic_CC])

        Monitor_Data.Monitor_Data_increment_total_database_UDP()
      except KeyboardInterrupt:
        if self.log_level >= vrb.INFO:
          self.logger.info('Closing UDP process..')
        return
