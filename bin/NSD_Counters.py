# Class to count the packets received and flow

# Imports python libraries
from multiprocessing import Lock, Manager
import logging


class NSD_Counters:

    __manager = Manager()
    __lock = __manager.Lock()

    Counter_Received_Total_ICMP = __manager.Value('i', 0)
    Counter_Received_Total_TCP = __manager.Value('i', 0)
    Counter_Received_Total_UDP = __manager.Value('i', 0)

    Counter_Database_Total_ICMP = __manager.Value('i', 0)
    Counter_Database_Total_TCP = __manager.Value('i', 0)
    Counter_Database_Total_UDP = __manager.Value('i', 0)

    Counter_Flows_ICMP = __manager.dict()
    Counter_Flows_TCP = __manager.dict()
    Counter_Flows_UDP = __manager.dict()


    # Increment total received
    @staticmethod
    def NSD_Counters_increment_total_received_ICMP():
        with NSD_Counters.__lock:
            NSD_Counters.Counter_Received_Total_ICMP.value += 1

    @staticmethod
    def NSD_Counters_increment_total_received_TCP():
        with NSD_Counters.__lock:
            NSD_Counters.Counter_Received_Total_TCP.value += 1

    @staticmethod
    def NSD_Counters_increment_total_received_UDP():
        with NSD_Counters.__lock:
            NSD_Counters.Counter_Received_Total_UDP.value += 1

    # Increment total packets inserted in the database
    @staticmethod
    def NSD_Counters_increment_total_database_ICMP():
        with NSD_Counters.__lock:
            NSD_Counters.Counter_Database_Total_ICMP.value += 1

    @staticmethod
    def NSD_Counters_increment_total_database_TCP():
        with NSD_Counters.__lock:
            NSD_Counters.Counter_Database_Total_TCP.value += 1

    @staticmethod
    def NSD_Counters_increment_total_database_UDP():
        with NSD_Counters.__lock:
            NSD_Counters.Counter_Database_Total_UDP.value += 1

    # Get total received
    @staticmethod
    def NSD_Counters_get_total_received_ICMP():
        with NSD_Counters.__lock:
            return NSD_Counters.Counter_Received_Total_ICMP.value

    @staticmethod
    def NSD_Counters_get_total_received_TCP():
        with NSD_Counters.__lock:
            return NSD_Counters.Counter_Received_Total_TCP.value

    @staticmethod
    def NSD_Counters_get_total_received_UDP():
        with NSD_Counters.__lock:
            return NSD_Counters.Counter_Received_Total_UDP.value

    # Get total database
    @staticmethod
    def NSD_Counters_get_total_database_ICMP():
        with NSD_Counters.__lock:
            return NSD_Counters.Counter_Database_Total_ICMP.value

    @staticmethod
    def NSD_Counters_get_total_database_TCP():
        with NSD_Counters.__lock:
            return NSD_Counters.Counter_Database_Total_TCP.value

    @staticmethod
    def NSD_Counters_get_total_database_UDP():
        with NSD_Counters.__lock:
            return NSD_Counters.Counter_Database_Total_UDP.value

    # Increment or add flow
    @staticmethod
    def NSD_Counters_update_flow_ICMP(flow, counter):
        with NSD_Counters.__lock:
            NSD_Counters.Counter_Flows_ICMP[flow] = counter

    @staticmethod
    def NSD_Counters_update_flow_TCP(flow, counter):
        with NSD_Counters.__lock:
            NSD_Counters.Counter_Flows_TCP[flow] = counter

    @staticmethod
    def NSD_Counters_update_flow_UDP(flow, counter):
        with NSD_Counters.__lock:
            NSD_Counters.Counter_Flows_UDP[flow] = counter

    # Get flows
    @staticmethod
    def NSD_Counters_get_flows_ICMP():
        with NSD_Counters.__lock:
            flows = []
            for flow in dict(NSD_Counters.Counter_Flows_ICMP):
                flows.append([flow, NSD_Counters.Counter_Flows_ICMP[flow], 0])
            return flows

    @staticmethod
    def NSD_Counters_get_flows_TCP():
        with NSD_Counters.__lock:
            flows = []
            for flow in dict(NSD_Counters.Counter_Flows_TCP):
                flows.append([flow, NSD_Counters.Counter_Flows_TCP[flow], 0])
            return flows

    @staticmethod
    def NSD_Counters_get_flows_UDP():
        with NSD_Counters.__lock:
            flows = []
            for flow in dict(NSD_Counters.Counter_Flows_UDP):
                flows.append([flow, NSD_Counters.Counter_Flows_UDP[flow], 0])
            return flows

    @staticmethod
    def NSD_Counters_get_flow_ICMP(flow):
        with NSD_Counters.__lock:
            try:
                return NSD_Counters.Counter_Flows_ICMP[flow]
            except KeyError as ke:
                return 0

    @staticmethod
    def NSD_Counters_get_flow_TCP(flow):
        with NSD_Counters.__lock:
            try:
                return NSD_Counters.Counter_Flows_TCP[flow]
            except KeyError as ke:
                return 0

    @staticmethod
    def NSD_Counters_get_flow_UDP(flow):
        with NSD_Counters.__lock:
            try:
                return NSD_Counters.Counter_Flows_UDP[flow]
            except KeyError as ke:
                return 0



