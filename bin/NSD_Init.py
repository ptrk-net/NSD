# Main class

# Imports python libraries
import sys
import logging
from multiprocessing import Process, Queue, Pipe
import multiprocessing

# Imports NSD libraries
from bin.NSD_Network import NSD_Network
from bin.NSD_Packets_Queue import NSD_Packets_Queue
from bin.NSD_Process import NSD_Process
from bin.NSD_Counters import NSD_Counters
from bin.NSD_Monitor import NSD_Monitor
from bin.NSD_Pcap import NSD_Pcap
from bin.NSD_Flow import NSD_Flow
from conf import settings as cfg


# Main
class NSD_Init:

    # Init function
    def __init__(self, daemon, pcap_file):
        # Create the variables
        self.logger = logging.getLogger(__name__)
        if daemon:
            self.logger.info('Starting as daemon..')
        else:
            self.logger.info('Preparing for analyze a PCAP file..')

        self.Procs = []
        self.Counters = NSD_Counters(cfg.LOGGING_LEVEL)
        self.Mon_Pipe_Parent, Mon_Pipe_Child = Pipe()
        self.Sync_Queue = Queue()
        self.Pkts_Queue = NSD_Packets_Queue(cfg.LOGGING_LEVEL)
        self.Mon_Proc = NSD_Monitor(cfg.LOGGING_LEVEL, self.Counters, Mon_Pipe_Child)
        self.Pkts_Proc = NSD_Process(cfg.LOGGING_LEVEL, cfg.TEMPORAL_DB_SERVER, cfg.TEMPORAL_DB_PORT, self.Counters, self.Sync_Queue)
        self.Flows_Proc = NSD_Flow(cfg.LOGGING_LEVEL, cfg.TEMPORAL_DB_SERVER, cfg.TEMPORAL_DB_PORT, self.Counters, self.Sync_Queue)

        if daemon:
            self.Net_Proc = NSD_Network(cfg.LOGGING_LEVEL, cfg.NETWORK_INTERFACE, self.Counters, self.Pkts_Queue, self.Sync_Queue,
                                    cfg.PROTOCOLS_FILE)
        else:
            self.Pcap_Proc = NSD_Pcap(cfg.LOGGING_LEVEL, pcap_file, self.Counters, self.Pkts_Queue, self.Sync_Queue, cfg.PROTOCOLS_FILE)

    # To manage the global interruptions
    def NSD_Init_except_hook(self, exctype, value, traceback):
        if exctype == KeyboardInterrupt:
            print("NSD_Init: INFO: Shutdown activated")
            for proc in multiprocessing.active_children():
                proc.terminate()
        else:
            sys.__excepthook__(exctype, value, traceback)

    # Create the environment necessary to work
    def NSD_Init_startup(self):

        # Create the monitor process
        self.logger.info('Starting up the monitor process...')
        Mon_P = Process(target=self.Mon_Proc.NSD_Monitor_process, args=())
        Mon_P.daemon = True
        Mon_P.start()
        self.Procs.append(Mon_P)
        self.logger.info('Monitor started!')

        # Create the process to process the packets based in the protocol
        self.logger.info('Starting up the TCP processing process...')
        for i in range(0, cfg.TCP_NUMBER_PROCESS):
            print('Starting ' + str(i) + ' TCP process..')
            TCP_PP = Process(target=self.Pkts_Proc.NSD_Process_live_TCP, args=(self.Pkts_Queue.TCP_Queue,))
            TCP_PP.daemon = True
            TCP_PP.start()
            self.Procs.append(TCP_PP)
        self.logger.info('TCP processing started!')

        self.logger.info('Starting up the UDP processing process...')
        for i in range(0, cfg.UDP_NUMBER_PROCESS):
            print('Starting ' + str(i) + ' UDP process..')
            UDP_PP = Process(target=self.Pkts_Proc.NSD_Process_live_UDP, args=(self.Pkts_Queue.UDP_Queue,))
            UDP_PP.daemon = True
            UDP_PP.start()
            self.Procs.append(UDP_PP)
        self.logger.info('UDP processing started!')

        self.logger.info('Starting up the ICMP processing process...')
        for i in range(0, cfg.ICMP_NUMBER_PROCESS):
            print('Starting ' + str(i) + ' ICMP process..')
            ICMP_PP = Process(target=self.Pkts_Proc.NSD_Process_live_ICMP, args=(self.Pkts_Queue.ICMP_Queue,))
            ICMP_PP.daemon = True
            ICMP_PP.start()
            self.Procs.append(ICMP_PP)
        self.logger.info('ICMP processing started!')

        # Create the Flows process
        print('Starting ICMP Flows process..')
        ICMP_FP = Process(target=self.Flows_Proc.NSD_Flow_ICMP, args=())
        ICMP_FP.daemon = True
        ICMP_FP.start()
        self.Procs.append(ICMP_FP)
        self.logger.info('ICMP Flows started!')

        print('Starting TCP Flows process..')
        TCP_FP = Process(target=self.Flows_Proc.NSD_Flow_TCP, args=())
        TCP_FP.daemon = True
        TCP_FP.start()
        self.Procs.append(TCP_FP)
        self.logger.info('TCP Flows started!')

        print('Starting UDP Flows process..')
        UDP_FP = Process(target=self.Flows_Proc.NSD_Flow_UDP, args=())
        UDP_FP.daemon = True
        UDP_FP.start()
        self.Procs.append(UDP_FP)
        self.logger.info('UDP Flows started!')

        # Create the AI process
        self.logger.info('Implementing AI process..')

        sys.excepthook = self.NSD_Init_except_hook


    # Start as daemon
    def NSD_Init_daemon(self):
        # Create the network process
        self.logger.info('Starting up the network process...')
        NP = Process(target=self.Net_Proc.NSD_Network_rcv, args=())
        NP.daemon = True
        NP.start()
        self.Procs.append(NP)
        self.logger.info('Network started!')

        while True:
            [protocol, value] = self.Mon_Pipe_Parent.recv()
            self.logger.warning(protocol + ' protocol needs ' + str(value) + 'process more!')
            sys.exit()

    # Start to analyze a PCAP file
    def NSD_Init_analyze_pcap(self):
        self.Pcap_Proc.NSD_Pcap_process()

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
