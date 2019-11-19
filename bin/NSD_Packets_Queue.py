# Class to add the packet to the processing queue

# Imports python libraries
from multiprocessing import Queue
import logging


# Class to process protocols-based queues
class NSD_Packets_Queue:

    # NSD
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.TCP_Queue = Queue()
        self.UDP_Queue = Queue()
        self.ICMP_Queue = Queue()

    # Process
    def NSD_Packets_Queue_insert_HOPOPT(self, packet):
        raise NotImplementedError('developing HOPOPT..')

    def NSD_Packets_Queue_insert_IP(self, packet):
        raise NotImplementedError('developing IP..')

    def NSD_Packets_Queue_insert_ICMP(self, packet):
        self.ICMP_Queue.put(packet)

    def NSD_Packets_Queue_insert_IGMP(self, packet):
        raise NotImplementedError('developing IGMP..')

    def NSD_Packets_Queue_insert_SCTP(self, packet):
        raise NotImplementedError('developing SCTP..')

    def NSD_Packets_Queue_insert_TCP(self, packet):
        self.TCP_Queue.put(packet)

    def NSD_Packets_Queue_insert_EGP(self, packet):
        raise NotImplementedError('developing EGP..')

    def NSD_Packets_Queue_insert_PUP(self, packet):
        raise NotImplementedError('developing PUP..')

    def NSD_Packets_Queue_insert_UDP(self, packet):
        self.UDP_Queue.put(packet)

    def NSD_Packets_Queue_insert_IDP(self, packet):
        raise NotImplementedError('developing IDP..')

    def NSD_Packets_Queue_insert_IPIP(self, packet):
        raise NotImplementedError('developing IPIP..')

    def NSD_Packets_Queue_insert_TP(self, packet):
        raise NotImplementedError('developing TP..')

    def NSD_Packets_Queue_insert_PIM(self, packet):
        raise NotImplementedError('developing PIM..')

    def NSD_Packets_Queue_insert_IPV6(self, packet):
        raise NotImplementedError('developing IPV6..')

    def NSD_Packets_Queue_insert_ROUTING(self, packet):
        raise NotImplementedError('developing ROUTING..')

    def NSD_Packets_Queue_insert_FRAGMENT(self, packet):
        raise NotImplementedError('developing FRAGMENT..')

    def NSD_Packets_Queue_insert_RSVP(self, packet):
        raise NotImplementedError('developing RSVP..')

    def NSD_Packets_Queue_insert_GRE(self, packet):
        raise NotImplementedError('developing GRE..')

    def NSD_Packets_Queue_insert_ESP(self, packet):
        raise NotImplementedError('developing ESP..')

    def NSD_Packets_Queue_insert_AH(self, packet):
        raise NotImplementedError('developing AH..')

    def NSD_Packets_Queue_insert_ICMPV6(self, packet):
        raise NotImplementedError('developing ICMPV6..')

    def NSD_Packets_Queue_insert_NONE(self, packet):
        raise NotImplementedError('developing NONE..')

    def NSD_Packets_Queue_insert_DSTOPTS(self, packet):
        raise NotImplementedError('developing DSTOPTS..')

    def NSD_Packets_Queue_insert_RAW(self, packet):
        raise NotImplementedError('developing RAW..')

    def NSD_Packets_Queue_insert_SSCOPMCE(self, packet):
        raise NotImplementedError('developing SSCOPMCE..')
