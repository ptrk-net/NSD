# Class to count the packets received and flow

# Imports python libraries
from multiprocessing import Manager
#import logging


class NSD_Monitor_Data:

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
    Status_Flows_ICMP = __manager.dict()
    Status_Flows_TCP = __manager.dict()
    Status_Flows_UDP = __manager.dict()


    # Increment total received
    @staticmethod
    def NSD_Monitor_Data_increment_total_received_ICMP():
        with NSD_Monitor_Data.__lock:
            NSD_Monitor_Data.Counter_Received_Total_ICMP.value += 1

    @staticmethod
    def NSD_Monitor_Data_increment_total_received_TCP():
        with NSD_Monitor_Data.__lock:
            NSD_Monitor_Data.Counter_Received_Total_TCP.value += 1

    @staticmethod
    def NSD_Monitor_Data_increment_total_received_UDP():
        with NSD_Monitor_Data.__lock:
            NSD_Monitor_Data.Counter_Received_Total_UDP.value += 1

    # Increment total packets inserted in the database
    @staticmethod
    def NSD_Monitor_Data_increment_total_database_ICMP():
        with NSD_Monitor_Data.__lock:
            NSD_Monitor_Data.Counter_Database_Total_ICMP.value += 1

    @staticmethod
    def NSD_Monitor_Data_increment_total_database_TCP():
        with NSD_Monitor_Data.__lock:
            NSD_Monitor_Data.Counter_Database_Total_TCP.value += 1

    @staticmethod
    def NSD_Monitor_Data_increment_total_database_UDP():
        with NSD_Monitor_Data.__lock:
            NSD_Monitor_Data.Counter_Database_Total_UDP.value += 1

    # Get total received
    @staticmethod
    def NSD_Monitor_Data_get_total_received_ICMP():
        with NSD_Monitor_Data.__lock:
            return NSD_Monitor_Data.Counter_Received_Total_ICMP.value

    @staticmethod
    def NSD_Monitor_Data_get_total_received_TCP():
        with NSD_Monitor_Data.__lock:
            return NSD_Monitor_Data.Counter_Received_Total_TCP.value

    @staticmethod
    def NSD_Monitor_Data_get_total_received_UDP():
        with NSD_Monitor_Data.__lock:
            return NSD_Monitor_Data.Counter_Received_Total_UDP.value

    # Get total database
    @staticmethod
    def NSD_Monitor_Data_get_total_database_ICMP():
        with NSD_Monitor_Data.__lock:
            return NSD_Monitor_Data.Counter_Database_Total_ICMP.value

    @staticmethod
    def NSD_Monitor_Data_get_total_database_TCP():
        with NSD_Monitor_Data.__lock:
            return NSD_Monitor_Data.Counter_Database_Total_TCP.value

    @staticmethod
    def NSD_Monitor_Data_get_total_database_UDP():
        with NSD_Monitor_Data.__lock:
            return NSD_Monitor_Data.Counter_Database_Total_UDP.value

    # Increment or add flow
    @staticmethod
    def NSD_Monitor_Data_update_counter_flow_ICMP(flow, counter):
        with NSD_Monitor_Data.__lock:
            NSD_Monitor_Data.Counter_Flows_ICMP[flow] = counter

    @staticmethod
    def NSD_Monitor_Data_update_counter_flow_TCP(flow, counter):
        with NSD_Monitor_Data.__lock:
            NSD_Monitor_Data.Counter_Flows_TCP[flow] = counter

    @staticmethod
    def NSD_Monitor_Data_update_counter_flow_UDP(flow, counter):
        with NSD_Monitor_Data.__lock:
            NSD_Monitor_Data.Counter_Flows_UDP[flow] = counter

    # Get flows
    @staticmethod
    def NSD_Monitor_Data_get_flows_ICMP():
        with NSD_Monitor_Data.__lock:
            flows = []
            for flow in dict(NSD_Monitor_Data.Counter_Flows_ICMP):
                flows.append([flow, NSD_Monitor_Data.Counter_Flows_ICMP[flow],
                              NSD_Monitor_Data.Status_Flows_ICMP[flow]])
            return flows

    @staticmethod
    def NSD_Monitor_Data_get_flows_TCP():
        with NSD_Monitor_Data.__lock:
            flows = []
            for flow in dict(NSD_Monitor_Data.Counter_Flows_TCP):
                flows.append([flow, NSD_Monitor_Data.Counter_Flows_TCP[flow],
                              NSD_Monitor_Data.Status_Flows_TCP[flow]])
            return flows

    @staticmethod
    def NSD_Monitor_Data_get_flows_UDP():
        with NSD_Monitor_Data.__lock:
            flows = []
            for flow in dict(NSD_Monitor_Data.Counter_Flows_UDP):
                flows.append([flow, NSD_Monitor_Data.Counter_Flows_UDP[flow], "ok"])
                              #NSD_Monitor_Data.Status_Flows_UDP[flow]])

            return flows

    # Get a flow's counter
    @staticmethod
    def NSD_Monitor_Data_get_counter_flow_ICMP(flow):
        with NSD_Monitor_Data.__lock:
            try:
                return NSD_Monitor_Data.Counter_Flows_ICMP[flow]
            except KeyError as ke:
                return None

    @staticmethod
    def NSD_Monitor_Data_get_counter_flow_TCP(flow):
        with NSD_Monitor_Data.__lock:
            try:
                return NSD_Monitor_Data.Counter_Flows_TCP[flow]
            except KeyError as ke:
                return None

    @staticmethod
    def NSD_Monitor_Data_get_counter_flow_UDP(flow):
        with NSD_Monitor_Data.__lock:
            try:
                return NSD_Monitor_Data.Counter_Flows_UDP[flow]
            except KeyError as ke:
                return None

    # Get a flow's status
    @staticmethod
    def NSD_Monitor_Data_get_status_flow_ICMP(flow):
        with NSD_Monitor_Data.__lock:
            try:
                return NSD_Monitor_Data.Status_Flows_ICMP[flow]
            except KeyError as ke:
                return None

    @staticmethod
    def NSD_Monitor_Data_get_status_flow_TCP(flow):
        with NSD_Monitor_Data.__lock:
            try:
                return NSD_Monitor_Data.Status_Flows_TCP[flow]
            except KeyError as ke:
                return None

    @staticmethod
    def NSD_Monitor_Data_get_status_flow_UDP(flow):
        with NSD_Monitor_Data.__lock:
            try:
                return NSD_Monitor_Data.Status_Flows_UDP[flow]
            except KeyError as ke:
                return None

    # Update or create a flow's status
    @staticmethod
    def NSD_Monitor_Data_update_status_flow_ICMP(flow, status):
        with NSD_Monitor_Data.__lock:
            NSD_Monitor_Data.Status_Flows_ICMP[flow] = status

    @staticmethod
    def NSD_Monitor_Data_update_status_flow_TCP(flow, status):
        with NSD_Monitor_Data.__lock:
            NSD_Monitor_Data.Status_Flows_TCP[flow] = status

    @staticmethod
    def NSD_Monitor_Data_update_status_flow_UDP(flow, status):
        with NSD_Monitor_Data.__lock:
            NSD_Monitor_Data.Status_Flows_UDP[flow] = status

