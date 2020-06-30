# Monitor class

# Imports python libraries
import time
import logging
from multiprocessing import Manager

# Import local libraries
from conf import variables as vrb


# Class to monitor the app
class Monitor:

  # init method
  def __init__(self, log_level, sync_queue):
    self.log_level = log_level
    self.logger = logging.getLogger(__name__)
    self.SQ = sync_queue
    self.__status_matrix = [['FLOW', ['UPDATING', 'STANDBY', 'FINISHED', 'ARCHIVED']],
                            ['AI', ['NOT_STARTED',
                                    'PT1_WORKING', 'PT1_WAITING', 'PT1_FINISHED',
                                    'PS12_WORKING', 'PS12_WAITING', 'PS12_FINISHED',
                                    ]],
                            ['RESULT', ['POSITIVE', 'NEGATIVE', 'SUSPECT']]]

  # Return the string that identifies a status
  # TODO: it's manually done, should be read from 'variables' file
  def __Monitor_get_name_status(self, type_status, status):
    return str(self.__status_matrix[type_status][0] + ': ' + self.__status_matrix[type_status][1][status])

  # monitor process
  def Monitor_process(self, pcap=False):
    if self.log_level < vrb.INFO:
      return 0

    while True:
      TCP_received_packets = Monitor_Data.Monitor_Data_get_total_received_TCP()
      UDP_received_packets = Monitor_Data.Monitor_Data_get_total_received_UDP()
      ICMP_received_packets = Monitor_Data.Monitor_Data_get_total_received_ICMP()
      ERROR_received_packets = Monitor_Data.Monitor_Data_get_total_received_ERROR()
      TCP_database_packets = Monitor_Data.Monitor_Data_get_total_database_TCP()
      UDP_database_packets = Monitor_Data.Monitor_Data_get_total_database_UDP()
      ICMP_database_packets = Monitor_Data.Monitor_Data_get_total_database_ICMP()
      ERROR_database_packets = Monitor_Data.Monitor_Data_get_total_database_ERROR()
      TCP_flows = Monitor_Data.Monitor_Data_get_flows_TCP()
      UDP_flows = Monitor_Data.Monitor_Data_get_flows_UDP()
      ICMP_flows = Monitor_Data.Monitor_Data_get_flows_ICMP()
      TCP_counter_flows = Monitor_Data.Monitor_Data_get_total_flows_TCP()
      UDP_counter_flows = Monitor_Data.Monitor_Data_get_total_flows_UDP()
      ICMP_counter_flows = Monitor_Data.Monitor_Data_get_total_flows_ICMP()
      RTP_counter_flows = Monitor_Data.Monitor_Data_get_total_flows_RTP()

      pkts_origin = 'Received' if not pcap else 'Read'

      self.logger.info('------------------------ PACKET LIVE REPORT -------------------------')
      self.logger.info('-- {}:'.format(pkts_origin))
      self.logger.info('   TCP|UDP|RTP|ICMP|ERROR|TOTAL: {}|{}|{}|{}|{}'.
                       format(TCP_received_packets, UDP_received_packets, ICMP_received_packets,
                              ERROR_received_packets,
                              TCP_received_packets + UDP_received_packets + ICMP_received_packets + ERROR_received_packets))
      self.logger.info('-- Inserted into the database:')
      self.logger.info('   TCP|UDP|RTP|ICMP|ERROR|TOTAL: {}|{}|{}|{}|{}'.
                       format(TCP_database_packets, UDP_database_packets, ICMP_database_packets,
                              ERROR_database_packets,
                              TCP_database_packets + UDP_database_packets + ICMP_database_packets + ERROR_database_packets))
      self.logger.info('-- Conversations identified:')
      self.logger.info('   TCP|UDP|RTP|ICMP|TOTAL: {}|{}|{}|{}'.
                       format(TCP_counter_flows, UDP_counter_flows, RTP_counter_flows, ICMP_counter_flows,
                              TCP_counter_flows + UDP_counter_flows + ICMP_counter_flows + RTP_counter_flows))
      self.logger.info('')

      """
      if TCP_received_packets > TCP_database_packets:
          self.Pipe.send(['TCP', 1])
      if UDP_received_packets > UDP_database_packets:
          self.Pipe.send(['UDP', 1])
      if ICMP_received_packets > ICMP_database_packets:
          self.Pipe.send(['ICMP', 1])
      """
      time.sleep(30)

  def Monitor_print_last_report(self, pcap=False):
    TCP_received_packets = Monitor_Data.Monitor_Data_get_total_received_TCP()
    UDP_received_packets = Monitor_Data.Monitor_Data_get_total_received_UDP()
    ICMP_received_packets = Monitor_Data.Monitor_Data_get_total_received_ICMP()
    ERROR_received_packets = Monitor_Data.Monitor_Data_get_total_received_ERROR()
    TCP_database_packets = Monitor_Data.Monitor_Data_get_total_database_TCP()
    UDP_database_packets = Monitor_Data.Monitor_Data_get_total_database_UDP()
    ICMP_database_packets = Monitor_Data.Monitor_Data_get_total_database_ICMP()
    ERROR_database_packets = Monitor_Data.Monitor_Data_get_total_database_ERROR()

    pkts_origin = 'Received' if not pcap else 'Read'

    self.logger.info('------------------------ PACKET SESSION REPORT -------------------------')
    self.logger.info('-- {}:'.format(pkts_origin))
    self.logger.info('   TCP|UDP|ICMP|ERROR|TOTAL: {}|{}|{}|{}|{}'.
                     format(TCP_received_packets, UDP_received_packets, ICMP_received_packets,
                            ERROR_received_packets,
                            TCP_received_packets + UDP_received_packets + ICMP_received_packets + ERROR_received_packets))
    self.logger.info('-- Inserted into the database:')
    self.logger.info('   TCP|UDP|ICMP|ERROR|TOTAL: {}|{}|{}|{}|{}'.
                     format(TCP_database_packets, UDP_database_packets, ICMP_database_packets,
                            ERROR_database_packets,
                            TCP_database_packets + UDP_database_packets + ICMP_database_packets + ERROR_database_packets))


class Monitor_Data:
  __manager = Manager()
  __lock = __manager.Lock()

  Counter_Received_Total_ICMP = __manager.Value('i', 0)
  Counter_Received_Total_TCP = __manager.Value('i', 0)
  Counter_Received_Total_UDP = __manager.Value('i', 0)
  Counter_Received_Total_ERROR = __manager.Value('i', 0)

  Counter_Database_Total_ICMP = __manager.Value('i', 0)
  Counter_Database_Total_TCP = __manager.Value('i', 0)
  Counter_Database_Total_UDP = __manager.Value('i', 0)
  Counter_Database_Total_ERROR = __manager.Value('i', 0)

  Counter_Flows_ICMP = __manager.dict()
  Counter_Flows_TCP = __manager.dict()
  Counter_Flows_UDP = __manager.dict()
  Counter_Flows_RTP = __manager.dict()
  Status_Flows_ICMP = __manager.dict()
  Status_Flows_TCP = __manager.dict()
  Status_Flows_UDP = __manager.dict()
  Status_Flows_RTP = __manager.dict()

  Counter_Total_Flows_ICMP = __manager.Value('i', 0)
  Counter_Total_Flows_TCP = __manager.Value('i', 0)
  Counter_Total_Flows_UDP = __manager.Value('i', 0)
  Counter_Total_Flows_RTP = __manager.Value('i', 0)

  # Increment total received
  @staticmethod
  def Monitor_Data_increment_total_received_ICMP():
    with Monitor_Data.__lock:
      Monitor_Data.Counter_Received_Total_ICMP.value += 1

  @staticmethod
  def Monitor_Data_increment_total_received_TCP():
    with Monitor_Data.__lock:
      Monitor_Data.Counter_Received_Total_TCP.value += 1

  @staticmethod
  def Monitor_Data_increment_total_received_UDP():
    with Monitor_Data.__lock:
      Monitor_Data.Counter_Received_Total_UDP.value += 1

  @staticmethod
  def Monitor_Data_increment_total_received_ERROR():
    with Monitor_Data.__lock:
      Monitor_Data.Counter_Received_Total_ERROR.value += 1

  # Increment total packets inserted in the database
  @staticmethod
  def Monitor_Data_increment_total_database_ICMP():
    with Monitor_Data.__lock:
      Monitor_Data.Counter_Database_Total_ICMP.value += 1

  @staticmethod
  def Monitor_Data_increment_total_database_TCP():
    with Monitor_Data.__lock:
      Monitor_Data.Counter_Database_Total_TCP.value += 1

  @staticmethod
  def Monitor_Data_increment_total_database_UDP():
    with Monitor_Data.__lock:
      Monitor_Data.Counter_Database_Total_UDP.value += 1

  @staticmethod
  def Monitor_Data_increment_total_database_ERROR():
    with Monitor_Data.__lock:
      Monitor_Data.Counter_Database_Total_ERROR.value += 1

  # Get total received
  @staticmethod
  def Monitor_Data_get_total_received_ICMP():
    with Monitor_Data.__lock:
      return Monitor_Data.Counter_Received_Total_ICMP.value

  @staticmethod
  def Monitor_Data_get_total_received_TCP():
    with Monitor_Data.__lock:
      return Monitor_Data.Counter_Received_Total_TCP.value

  @staticmethod
  def Monitor_Data_get_total_received_UDP():
    with Monitor_Data.__lock:
      return Monitor_Data.Counter_Received_Total_UDP.value

  @staticmethod
  def Monitor_Data_get_total_received_ERROR():
    with Monitor_Data.__lock:
      return Monitor_Data.Counter_Received_Total_ERROR.value

  # Get total database
  @staticmethod
  def Monitor_Data_get_total_database_ICMP():
    with Monitor_Data.__lock:
      return Monitor_Data.Counter_Database_Total_ICMP.value

  @staticmethod
  def Monitor_Data_get_total_database_TCP():
    with Monitor_Data.__lock:
      return Monitor_Data.Counter_Database_Total_TCP.value

  @staticmethod
  def Monitor_Data_get_total_database_UDP():
    with Monitor_Data.__lock:
      return Monitor_Data.Counter_Database_Total_UDP.value

  @staticmethod
  def Monitor_Data_get_total_database_ERROR():
    with Monitor_Data.__lock:
      return Monitor_Data.Counter_Database_Total_ERROR.value

  # Increment or add flow
  @staticmethod
  def Monitor_Data_update_counter_flow_ICMP(flow, counter):
    with Monitor_Data.__lock:
      Monitor_Data.Counter_Flows_ICMP[flow] = counter

  @staticmethod
  def Monitor_Data_update_counter_flow_TCP(flow, counter):
    with Monitor_Data.__lock:
      Monitor_Data.Counter_Flows_TCP[flow] = counter

  @staticmethod
  def Monitor_Data_update_counter_flow_UDP(flow, counter):
    with Monitor_Data.__lock:
      Monitor_Data.Counter_Flows_UDP[flow] = counter

  @staticmethod
  def Monitor_Data_update_counter_flow_RTP(flow, counter):
    with Monitor_Data.__lock:
      Monitor_Data.Counter_Flows_RTP[flow] = counter

  # Increment number of total flows
  @staticmethod
  def Monitor_Data_update_counter_flows_ICMP():
    with Monitor_Data.__lock:
      Monitor_Data.Counter_Total_Flows_ICMP.value += 1

  @staticmethod
  def Monitor_Data_update_counter_flows_TCP():
    with Monitor_Data.__lock:
      Monitor_Data.Counter_Total_Flows_TCP.value += 1

  @staticmethod
  def Monitor_Data_update_counter_flows_UDP():
    with Monitor_Data.__lock:
      Monitor_Data.Counter_Total_Flows_UDP.value += 1

  @staticmethod
  def Monitor_Data_update_counter_flows_RTP():
    with Monitor_Data.__lock:
      Monitor_Data.Counter_Total_Flows_RTP.value += 1

  # Get flows
  @staticmethod
  def Monitor_Data_get_flows_ICMP():
    with Monitor_Data.__lock:
      flows = []
      for flow in dict(Monitor_Data.Counter_Flows_ICMP):
        flows.append([flow, Monitor_Data.Counter_Flows_ICMP[flow],
                      Monitor_Data.Status_Flows_ICMP[flow]])
      return flows

  @staticmethod
  def Monitor_Data_get_flows_TCP():
    with Monitor_Data.__lock:
      flows = []
      for flow in dict(Monitor_Data.Counter_Flows_TCP):
        flows.append([flow, Monitor_Data.Counter_Flows_TCP[flow],
                      Monitor_Data.Status_Flows_TCP[flow]])
      return flows

  @staticmethod
  def Monitor_Data_get_flows_UDP():
    with Monitor_Data.__lock:
      flows = []
      for flow in dict(Monitor_Data.Counter_Flows_UDP):
        flows.append([flow, Monitor_Data.Counter_Flows_UDP[flow],
                      Monitor_Data.Status_Flows_UDP[flow]])
    return flows

  @staticmethod
  def Monitor_Data_get_flows_RTP():
    with Monitor_Data.__lock:
      flows = []
      for flow in dict(Monitor_Data.Counter_Flows_RTP):
        flows.append([flow, Monitor_Data.Counter_Flows_RTP[flow],
                      Monitor_Data.Status_Flows_RTP[flow]])
    return flows

  # Get a flow's counter
  @staticmethod
  def Monitor_Data_get_counter_flow_ICMP(flow):
    with Monitor_Data.__lock:
      try:
        return Monitor_Data.Counter_Flows_ICMP[flow]
      except KeyError as ke:
        return None

  @staticmethod
  def Monitor_Data_get_counter_flow_TCP(flow):
    with Monitor_Data.__lock:
      try:
        return Monitor_Data.Counter_Flows_TCP[flow]
      except KeyError as ke:
        return None

  @staticmethod
  def Monitor_Data_get_counter_flow_UDP(flow):
    with Monitor_Data.__lock:
      try:
        return Monitor_Data.Counter_Flows_UDP[flow]
      except KeyError as ke:
        return None

  @staticmethod
  def Monitor_Data_get_counter_flow_RTP(flow):
    with Monitor_Data.__lock:
      try:
        return Monitor_Data.Counter_Flows_RTP[flow]
      except KeyError as ke:
        return None

  # Get a flow's status
  @staticmethod
  def Monitor_Data_get_status_flow_ICMP(flow):
    with Monitor_Data.__lock:
      try:
        return Monitor_Data.Status_Flows_ICMP[flow]
      except KeyError as ke:
        return None

  @staticmethod
  def Monitor_Data_get_status_flow_TCP(flow):
    with Monitor_Data.__lock:
      try:
        return Monitor_Data.Status_Flows_TCP[flow]
      except KeyError as ke:
        return None

  @staticmethod
  def Monitor_Data_get_status_flow_UDP(flow):
    with Monitor_Data.__lock:
      try:
        return Monitor_Data.Status_Flows_UDP[flow]
      except KeyError as ke:
        return None

  @staticmethod
  def Monitor_Data_get_status_flow_RTP(flow):
    with Monitor_Data.__lock:
      try:
        return Monitor_Data.Status_Flows_RTP[flow]
      except KeyError as ke:
        return None

  # Update or create a flow's status
  @staticmethod
  def Monitor_Data_update_status_flow_ICMP(flow, status):
    with Monitor_Data.__lock:
      Monitor_Data.Status_Flows_ICMP[flow] = status

  @staticmethod
  def Monitor_Data_update_status_flow_TCP(flow, status):
    with Monitor_Data.__lock:
      Monitor_Data.Status_Flows_TCP[flow] = status

  @staticmethod
  def Monitor_Data_update_status_flow_UDP(flow, status):
    with Monitor_Data.__lock:
      Monitor_Data.Status_Flows_UDP[flow] = status

  @staticmethod
  def Monitor_Data_update_status_flow_RTP(flow, status):
    with Monitor_Data.__lock:
      Monitor_Data.Status_Flows_RTP[flow] = status

  # Get total flows
  @staticmethod
  def Monitor_Data_get_total_flows_ICMP():
    with Monitor_Data.__lock:
      return Monitor_Data.Counter_Total_Flows_ICMP.value

  @staticmethod
  def Monitor_Data_get_total_flows_TCP():
    with Monitor_Data.__lock:
      return Monitor_Data.Counter_Total_Flows_TCP.value

  @staticmethod
  def Monitor_Data_get_total_flows_UDP():
    with Monitor_Data.__lock:
      return Monitor_Data.Counter_Total_Flows_UDP.value

  @staticmethod
  def Monitor_Data_get_total_flows_RTP():
    with Monitor_Data.__lock:
      return Monitor_Data.Counter_Total_Flows_RTP.value
