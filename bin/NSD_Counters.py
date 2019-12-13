# Class to count the packets received and flow

# Imports python libraries
from multiprocessing import Value, Lock
import logging


class NSD_Counters:
    def __init__(self, log_level, initial_value=0):
        self.log_level = log_level
        self.logger = logging.getLogger(__name__)
        self.lock = Lock()

        self.Received_Counter_Total_ICMP = Value('i', initial_value)
        self.Received_Counter_Total_TCP = Value('i', initial_value)
        self.Received_Counter_Total_UDP = Value('i', initial_value)

        self.Database_Counter_Total_ICMP = Value('i', initial_value)
        self.Database_Counter_Total_TCP = Value('i', initial_value)
        self.Database_Counter_Total_UDP = Value('i', initial_value)

        self.Counter_Flow_ICMP = {}
        self.Counter_Flow_TCP = {}
        self.Counter_Flow_UDP = {}

    # Increment total received
    def NSD_Counters_increment_total_received_ICMP(self):
        with self.lock:
            self.Received_Counter_Total_ICMP.value += 1

    def NSD_Counters_increment_total_received_TCP(self):
        with self.lock:
            self.Received_Counter_Total_TCP.value += 1

    def NSD_Counters_increment_total_received_UDP(self):
        with self.lock:
            self.Received_Counter_Total_UDP.value += 1

    # Increment total packets inserted in the database
    def NSD_Counters_increment_total_database_ICMP(self):
        with self.lock:
            self.Database_Counter_Total_ICMP.value += 1

    def NSD_Counters_increment_total_database_TCP(self):
        with self.lock:
            self.Database_Counter_Total_TCP.value += 1

    def NSD_Counters_increment_total_database_UDP(self):
        with self.lock:
            self.Database_Counter_Total_UDP.value += 1

    # Get total received
    def NSD_Counters_get_total_received_ICMP(self):
        with self.lock:
            return self.Received_Counter_Total_ICMP.value

    def NSD_Counters_get_total_received_TCP(self):
        with self.lock:
            return self.Received_Counter_Total_TCP.value

    def NSD_Counters_get_total_received_UDP(self):
        with self.lock:
            return self.Received_Counter_Total_UDP.value

    # Get total database
    def NSD_Counters_get_total_database_ICMP(self):
        with self.lock:
            return self.Database_Counter_Total_ICMP.value

    def NSD_Counters_get_total_database_TCP(self):
        with self.lock:
            return self.Database_Counter_Total_TCP.value

    def NSD_Counters_get_total_database_UDP(self):
        with self.lock:
            return self.Database_Counter_Total_UDP.value

    # Increment or add flow
    def NSD_Counters_update_flow_ICMP(self, flow, counter):
        with self.lock:
            self.Counter_Flow_ICMP.update([(flow, counter)])

    def NSD_Counters_update_flow_TCP(self, flow, counter):
        with self.lock:
            self.Counter_Flow_TCP.update([(flow, counter)])

    def NSD_Counters_update_flow_UDP(self, flow, counter):
        with self.lock:
            self.Counter_Flow_UDP.update([(flow, counter)])

    # Get flows
    def NSD_Counters_get_flow_ICMP(self, flow):
        with self.lock:
            try:
                return self.Counter_Flow_ICMP[flow]
            except KeyError as ke:
                self.logger.info('Flow id {0} does not exist at ICMP counter.'.format(flow))
                return 0

    def NSD_Counters_get_flow_TCP(self, flow):
        with self.lock:
            try:
                return self.Counter_Flow_TCP[flow]
            except KeyError as ke:
                self.logger.info('Flow id {0} does not exist at TCP counter.'.format(flow))
                return 0

    def NSD_Counters_get_flow_UDP(self, flow):
        with self.lock:
            try:
                return self.Counter_Flow_UDP[flow]
            except KeyError as ke:
                self.logger.info('Flow id {0} does not exist at UDP counter.'.format(flow))
                return 0
