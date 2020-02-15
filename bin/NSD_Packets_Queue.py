# Class to add the packet to the processing queue

# Imports python libraries
from multiprocessing import Queue
#import logging


# Class to process protocols-based queues
class NSD_Packets_Queue:

    # NSD
    def __init__(self, log_level):
        self.log_level = log_level
        #self.logger = logging.getLogger(__name__)
        self.TCP_Queue = Queue()
        self.UDP_Queue = Queue()
        self.ICMP_Queue = Queue()

    # Process
    def NSD_Packets_Queue_insert_ICMP(self, packet):
        self.ICMP_Queue.put(packet)

    def NSD_Packets_Queue_insert_TCP(self, packet):
        self.TCP_Queue.put(packet)

    def NSD_Packets_Queue_insert_UDP(self, packet):
        self.UDP_Queue.put(packet)

