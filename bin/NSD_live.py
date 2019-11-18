# import system libraries
import sys
from multiprocessing import Process, Queue, Pipe

# import NSD libraries
from bin.NSD_Network import NSD_Network
from bin.NSD_Packets_Queue import NSD_Packets_Queue
from bin.NSD_Process import NSD_Process
from bin.NSD_Counters import NSD_Counters
from bin.NSD_Monitor import NSD_Monitor

from conf import settings as cfg

# Main
if __name__ == '__main__':

	# Create de variables
	Procs = []
	Counters = NSD_Counters()
	Mon_Pipe_Parent, Mon_Pipe_Child = Pipe()
	Sync_Queue = Queue()
	Pkts_Queue = NSD_Packets_Queue()
	Mon_Proc = NSD_Monitor(Counters, Mon_Pipe_Child)
	Net_Proc = NSD_Network(cfg.NETWORK_INTERFACE, Counters, Pkts_Queue, Sync_Queue, cfg.PROTOCOLS_FILE)
	Pkts_Proc = NSD_Process(cfg.TEMPORAL_DB_SERVER, cfg.TEMPORAL_DB_PORT, Counters, Sync_Queue)

	# Create the monitor process
	Mon_P = Process(target=Mon_Proc.merc_monitor_process, args=())
	Mon_P.daemon = True
	Mon_P.start()
	Procs.append(Mon_P)

	# Create the process to process the packets based in the protocol
	for i in range(0, cfg.TCP_NUMBER_PROCESS):
		print('Starting ' + str(i) + ' TCP process..')
		TCP_PP = Process(target=Pkts_Proc.NSD_Process_live_TCP, args=(Pkts_Queue.TCP_Queue,))
		TCP_PP.daemon = True
		TCP_PP.start()
		Procs.append(TCP_PP)

	for i in range(0, cfg.UDP_NUMBER_PROCESS):
		print('Starting ' + str(i) + ' UDP process..')
		UDP_PP = Process(target=Pkts_Proc.NSD_Process_live_UDP, args=(Pkts_Queue.UDP_Queue,))
		UDP_PP.daemon = True
		UDP_PP.start()
		Procs.append(UDP_PP)

	for i in range(0, cfg.ICMP_NUMBER_PROCESS):
		print('Starting ' + str(i) + ' ICMP process..')
		ICMP_PP = Process(target=Pkts_Proc.NSD_Process_live_ICMP, args=(Pkts_Queue.ICMP_Queue,))
		ICMP_PP.daemon = True
		ICMP_PP.start()
		Procs.append(ICMP_PP)

	# Create the AI process

	# Create the network process
	print('Starting Network process..')
	NP = Process(target=Net_Proc.NSD_Network_rcv, args=())
	NP.daemon = True
	NP.start()
	Procs.append(NP)

	while True:
		[protocol, value] = Mon_Pipe_Parent.recv()
		print(protocol + ' protocol needs ' + str(value) + 'process more!')
		sys.exit()

	# Link all the process with main
	#for proc in Procs:
	#	proc.join()

	# Finish the program
	#while True:
	#	print('Waiting for the Sync Msg..')
	#	Msg = Sync_Queue.get()
	#	print(Msg)
	#	if Msg == 'KILL':
	#		for proc in Procs:
	#			proc.terminate()
	

