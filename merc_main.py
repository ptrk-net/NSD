# import system libraries
#import re
#import time
import sys
from multiprocessing import Process,Queue,Pipe

# import Merc libraries
from merc_network import Merc_Network
from merc_database import Merc_Database
from merc_packets_queue import Merc_Packets_Queue
from merc_processing import Merc_Processing
from merc_counters import Merc_Counters
from merc_monitor import Merc_Monitor

TCP_NUMBER_PROCESS = 10
UDP_NUMBER_PROCESS = 2
ICMP_NUMBER_PROCESS = 1

# Main
if __name__ == '__main__':

	# Create de variables
	Procs = []
	Counters = Merc_Counters()
	Mon_Pipe_Parent, Mon_Pipe_Child = Pipe()
	Sync_Queue = Queue()
	Pkts_Queue = Merc_Packets_Queue()
	Mon_Proc = Merc_Monitor(Counters, Mon_Pipe_Child)
	Net_Proc = Merc_Network('ens32', Counters, Pkts_Queue, Sync_Queue)
	Mem_DB = Merc_Database(True, Sync_Queue)
	Pkts_Proc = Merc_Processing(Counters, Mem_DB, Sync_Queue)

	# Create the monitor process
	Mon_P = Process(target=Mon_Proc.merc_monitor_process, args=())
	Mon_P.daemon = True
	Mon_P.start()
	Procs.append(Mon_P)

	# Create the process to process the packets based in the protocol
	for i in range(0, TCP_NUMBER_PROCESS):
		print('Starting ' + str(i) + ' TCP process..')
		TCP_PP = Process(target=Pkts_Proc.merc_processing_TCP, args=(Pkts_Queue.TCP_Queue,))
		TCP_PP.daemon = True
		TCP_PP.start()
		Procs.append(TCP_PP)

	for i in range(0, UDP_NUMBER_PROCESS):
		print('Starting ' + str(i) + ' UDP process..')
		UDP_PP = Process(target=Pkts_Proc.merc_processing_UDP, args=(Pkts_Queue.UDP_Queue,))
		UDP_PP.daemon = True
		UDP_PP.start()
		Procs.append(UDP_PP)

	for i in range(0, ICMP_NUMBER_PROCESS):
		print('Starting ' + str(i) + ' ICMP process..')
		ICMP_PP = Process(target=Pkts_Proc.merc_processing_ICMP, args=(Pkts_Queue.ICMP_Queue,))
		ICMP_PP.daemon = True
		ICMP_PP.start()
		Procs.append(ICMP_PP)

	# Create the AI process


	# Create the network process
	print('Starting Network process..')
	NP = Process(target=Net_Proc.merc_network_rcv, args=())
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
	

