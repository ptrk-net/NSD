# Main class

# Imports python libraries
import sys
import logging
from multiprocessing import Process, Queue, Pipe

# Imports NSD libraries
from bin.NSD_Network import NSD_Network
from bin.NSD_Packets_Queue import NSD_Packets_Queue
from bin.NSD_Process import NSD_Process
from bin.NSD_Counters import NSD_Counters
from bin.NSD_Monitor import NSD_Monitor

from conf import settings as cfg


# Main
class NSD_Main:

    def __init__(self, daemon, pcap_file):
        # Create the variables
        self.logger = logging.getLogger(__name__)
        self.Procs = []
        self.Counters = NSD_Counters()
        self.Mon_Pipe_Parent, Mon_Pipe_Child = Pipe()
        self.Sync_Queue = Queue()
        self.Pkts_Queue = NSD_Packets_Queue()
        self.Mon_Proc = NSD_Monitor(self.Counters, Mon_Pipe_Child)
        self.Pkts_Proc = NSD_Process(cfg.TEMPORAL_DB_SERVER, cfg.TEMPORAL_DB_PORT, self.Counters, self.Sync_Queue)

        if daemon:
            self.Net_Proc = NSD_Network(cfg.NETWORK_INTERFACE, self.Counters, self.Pkts_Queue, self.Sync_Queue,
                                    cfg.PROTOCOLS_FILE)
        else:
            self.Pcap_Proc = NSD_Pcap()


    def NSD_main_startup(self):
        # Create the monitor process

        self.logger.info('Starting up the monitor process...')
        Mon_P = Process(target=self.Mon_Proc.merc_monitor_process, args=())
        Mon_P.daemon = True
        Mon_P.start()
        self.Procs.append(Mon_P)

        # Create the process to process the packets based in the protocol
        self.logger.info('Starting up the TCP processing process...')
        for i in range(0, cfg.TCP_NUMBER_PROCESS):
            print('Starting ' + str(i) + ' TCP process..')
            TCP_PP = Process(target=self.Pkts_Proc.NSD_Process_live_TCP, args=(self.Pkts_Queue.TCP_Queue,))
            TCP_PP.daemon = True
            TCP_PP.start()
            self.Procs.append(TCP_PP)

        self.logger.info('Starting up the UDP processing process...')
        for i in range(0, cfg.UDP_NUMBER_PROCESS):
            print('Starting ' + str(i) + ' UDP process..')
            UDP_PP = Process(target=self.Pkts_Proc.NSD_Process_live_UDP, args=(self.Pkts_Queue.UDP_Queue,))
            UDP_PP.daemon = True
            UDP_PP.start()
            self.Procs.append(UDP_PP)

        self.logger.info('Starting up the ICMP processing process...')
        for i in range(0, cfg.ICMP_NUMBER_PROCESS):
            print('Starting ' + str(i) + ' ICMP process..')
            ICMP_PP = Process(target=self.Pkts_Proc.NSD_Process_live_ICMP, args=(self.Pkts_Queue.ICMP_Queue,))
            ICMP_PP.daemon = True
            ICMP_PP.start()
            self.Procs.append(ICMP_PP)

        # Create the AI process

        # Create the network process
        self.logger.info('Starting up the network process...')
        NP = Process(target=self.Net_Proc.NSD_Network_rcv, args=())
        NP.daemon = True
        NP.start()
        self.Procs.append(NP)

    def NSD_Main_daemon(self):
        while True:
            [protocol, value] = self.Mon_Pipe_Parent.recv()
            self.logger.warning(protocol + ' protocol needs ' + str(value) + 'process more!')
            sys.exit()

    def NSD_Main_read_pcap(self):
        raise NotImplementedError('Implementing..')

# Link all the process with main
# for proc in Procs:
#	proc.join()

# Finish the program
# while True:
#	print('Waiting for the Sync Msg..')
#	Msg = Sync_Queue.get()
#	print(Msg)
#	if Msg == 'KILL':
#		for proc in Procs:
#			proc.terminate()
