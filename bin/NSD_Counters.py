# Class to count the packets received and conversation

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

        self.Counter_Conversation_ICMP = {}
        self.Counter_Conversation_TCP = {}
        self.Counter_Conversation_UDP = {}

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

    # Add conversation
    def NSD_Counters_add_conversation_ICMP(self, conversation):
        with self.lock:
            self.Counter_Conversation_ICMP.update([(conversation, 1)])

    def NSD_Counters_add_conversation_TCP(self, conversation):
        with self.lock:
            self.Counter_Conversation_TCP.update([(conversation, 1)])

    def NSD_Counters_add_conversation_UDP(self, conversation):
        with self.lock:
            self.Counter_Conversation_UDP.update([(conversation, 1)])

    # Increment conversation
    def NSD_Counters_update_conversation_ICMP(self, conversation, counter):
        with self.lock:
            self.Counter_Conversation_ICMP.update([(conversation, counter)])

    def NSD_Counters_update_conversation_TCP(self, conversation, counter):
        with self.lock:
            self.Counter_Conversation_TCP.update([(conversation, counter)])

    def NSD_Counters_update_conversation_UDP(self, conversation, counter):
        with self.lock:
            self.Counter_Conversation_UDP.update([(conversation, counter)])

    # Get conversation
    def NSD_Counters_get_conversation_ICMP(self, conversation):
        with self.lock:
            try:
                return self.Counter_Conversation_ICMP[conversation]
            except KeyError as ke:
                self.logger.info('Conversation id {0} does not exist at ICMP counter.'.format(conversation))
                return 0

    def NSD_Counters_get_conversation_TCP(self, conversation):
        with self.lock:
            try:
                return self.Counter_Conversation_TCP[conversation]
            except KeyError as ke:
                self.logger.info('Conversation id {0} does not exist at TCP counter.'.format(conversation))
                return 0

    def NSD_Counters_get_conversation_UDP(self, conversation):
        with self.lock:
            try:
                return self.Counter_Conversation_UDP[conversation]
            except KeyError as ke:
                self.logger.info('Conversation id {0} does not exist at UDP counter.'.format(conversation))
                return 0
