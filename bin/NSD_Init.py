# Main class

# Imports python libraries
import sys
import logging
from multiprocessing import Process, Queue
from threading import Thread
import time

# Imports local libraries
from bin.NSD_Network import NSD_Network
from bin.NSD_Packets_Queue import NSD_Packets_Queue
from bin.NSD_Packets_Processor import NSD_Packets_Processor
from bin.NSD_Monitor import NSD_Monitor
from bin.NSD_Pcap import NSD_Pcap
from bin.NSD_Flow import NSD_Flow
from bin.NSD_ML import NSD_ML
from conf import settings as cfg
from conf import variables as vrb


# Main
class NSD_Init:

  # NSD_Init function
  def __init__(self, daemon, training, pcapfile, log_level):
    # Create the variables
    self.log_level = log_level if log_level >= cfg.LOGGING_LEVEL else cfg.LOGGING_FILE
    self.logger = logging.getLogger(__name__)

    db_name = cfg.DB_PCAP if len(pcapfile) == 1 else cfg.DB_NAME
    if self.log_level >= vrb.DEBUG:
      self.logger.debug('database name: {}'.format(db_name))

    if daemon and self.log_level >= vrb.INFO:
      self.logger.info('Starting as daemon..')
    elif training and self.log_level >= vrb.INFO:
      self.logger.info('Starting for training AI..')
    elif self.log_level >= vrb.INFO:
      self.logger.info('Preparing for analyze a PCAP file..')

    self.Procs = list()
    self.Sync_Queue = Queue()
    self.Mon_Proc = NSD_Monitor(self.log_level, self.Sync_Queue)

    self.ML_Proc = NSD_ML(self.log_level, self.Sync_Queue, db_name, daemon, training)

    if not pcapfile[0] or len(pcapfile) == 1 or not pcapfile[1]:
      self.Flows_Proc = NSD_Flow(self.log_level, cfg.DB_SERVER, cfg.DB_PORT, db_name, self.Sync_Queue)

    if not training:
      self.Pkts_Proc = NSD_Packets_Processor(self.log_level, cfg.DB_SERVER, cfg.DB_PORT, db_name, self.Sync_Queue,
                                             (1 if pcapfile[0] and len(pcapfile) == 2 and pcapfile[1] == 'covert' else
                                  0 if pcapfile[0] and len(pcapfile) == 2 and pcapfile[1] == 'overt' else 2))

    if daemon:
      self.Net_Proc = NSD_Network(self.log_level, cfg.NETWORK_INTERFACE, self.Sync_Queue)
    elif len(pcapfile) == 1 or pcapfile[0]:
      self.Pcap_Proc = NSD_Pcap(self.log_level, self.Sync_Queue, pcapfile)

  # To manage the global interruptions
  def except_hook(self, exctype, value, traceback):
    if exctype == KeyboardInterrupt:
      if self.log_level >= vrb.INFO:
        self.logger.info("NSD_Init: INFO: Shutdown activated")
      for proc in self.Procs:
        proc.terminate()
    else:
      sys.__excepthook__(exctype, value, traceback)

  # Create the environment necessary to work
  def startup(self, pcapfile, training):
    # Create the monitor process
    if self.log_level >= vrb.INFO:
      self.logger.info('Starting up the monitor process...')
    Mon_P = Process(target=self.Mon_Proc.show_info, args=((True if pcapfile else False),))
    Mon_P.daemon = True
    Mon_P.start()
    self.Procs.append(Mon_P)
    if self.log_level >= vrb.INFO:
      self.logger.info('NSD_Monitor started!')

    if not training:
      # Create the processes to get into the database the packets based in the protocol
      if self.log_level >= vrb.INFO:
        self.logger.info('Starting up the TCP processing process...')
      for i in range(0, cfg.TCP_NUMBER_PROCESS):
        if self.log_level >= vrb.INFO:
          self.logger.info('Starting {} TCP process..'.format(str(i)))
        TCP_PP = Process(target=self.Pkts_Proc.process_TCP_packets, args=())
        TCP_PP.daemon = True
        TCP_PP.start()
        self.Procs.append(TCP_PP)
      if self.log_level >= vrb.INFO:
        self.logger.info('TCP processing started!')

      if self.log_level >= vrb.INFO:
        self.logger.info('Starting up the UDP processing process...')
      for i in range(0, cfg.UDP_NUMBER_PROCESS):
        if self.log_level >= vrb.INFO:
          self.logger.info('Starting {} UDP process..'.format(str(i)))
        UDP_PP = Process(target=self.Pkts_Proc.process_UDP_packets, args=())
        UDP_PP.daemon = True
        UDP_PP.start()
        self.Procs.append(UDP_PP)
      if self.log_level >= vrb.INFO:
        self.logger.info('UDP processing started!')

      if self.log_level >= vrb.INFO:
        self.logger.info('Starting up the ICMP processing process...')
      for i in range(0, cfg.ICMP_NUMBER_PROCESS):
        if self.log_level >= vrb.INFO:
          self.logger.info('Starting {} ICMP process..'.format(str(i)))
        ICMP_PP = Process(target=self.Pkts_Proc.process_ICMP_packets, args=())
        ICMP_PP.daemon = True
        ICMP_PP.start()
        self.Procs.append(ICMP_PP)
      if self.log_level >= vrb.INFO:
        self.logger.info('ICMP processing started!')

    # Create the Flows process
    if len(pcapfile) != 2 or not pcapfile[0]:
      tagged = True if training else False

      if self.log_level >= vrb.INFO:
        self.logger.info('Starting ICMP Flows process..')
      ICMP_FP = Process(target=self.Flows_Proc.get_flow_ICMP, args=(tagged,))
      ICMP_FP.daemon = True
      ICMP_FP.start()
      self.Procs.append(ICMP_FP)
      if self.log_level >= vrb.INFO:
        self.logger.info('ICMP Flows started!')

      if self.log_level >= vrb.INFO:
        self.logger.info('Starting TCP Flows process..')
      TCP_FP = Process(target=self.Flows_Proc.get_flow_TCP, args=(tagged,))
      TCP_FP.daemon = True
      TCP_FP.start()
      self.Procs.append(TCP_FP)
      if self.log_level >= vrb.INFO:
        self.logger.info('TCP Flows started!')

      if self.log_level >= vrb.INFO:
        self.logger.info('Starting UDP Flows process..')
      UDP_FP = Process(target=self.Flows_Proc.get_flow_UDP, args=(tagged,))
      UDP_FP.daemon = True
      UDP_FP.start()
      self.Procs.append(UDP_FP)
      if self.log_level >= vrb.INFO:
        self.logger.info('UDP Flows started!')

      if self.log_level >= vrb.INFO:
        self.logger.info('Starting RTP Flows process..')
      RTP_FP = Process(target=self.Flows_Proc.get_flow_RTP, args=(tagged,))
      RTP_FP.daemon = True
      RTP_FP.start()
      self.Procs.append(RTP_FP)
      if self.log_level >= vrb.INFO:
        self.logger.info('RTP Flows started!')

  # Start process that need to be listened to
  def main_processing(self, daemon, training, pcapfile):
    if daemon:
      # Create the network process
      if self.log_level >= vrb.INFO:
        self.logger.info('Starting up the network process...')
      NP = Thread(target=self.Net_Proc.receiver, args=())
      NP.setDaemon(True)
      NP.start()
      self.Procs.append(NP)
      if self.log_level >= vrb.INFO:
        self.logger.info('NSD_Network started!')
    elif len(pcapfile) == 1 or pcapfile[0]:
      self.Pcap_Proc.process_pcapfile()
      if self.log_level >= vrb.INFO:
        self.logger.info('waiting for reading packets..')
      __pcap_finished = False
      while not __pcap_finished:
        msg = self.Sync_Queue.get()
        if msg == 'PCAP_FINISHED':
          __pcap_finished = True

    if training:
      MLP = Process(target=self.ML_Proc.training, args=(cfg.FEATURES, cfg.T, cfg.S))
      MLP.daemon = True
      MLP.start()
      self.Procs.append(MLP)
      if self.log_level >= vrb.INFO:
        self.logger.info('ML Training mode started!')
    elif len(pcapfile) == 1 or daemon:
      ML_GF_PP = Process(target=self.ML_Proc.get_RTP_features, args=(cfg.FEATURES, cfg.T, cfg.S))
      ML_GF_PP.daemon = True
      ML_GF_PP.start()
      self.Procs.append(ML_GF_PP)
      ML_EV_PP = Process(target=self.ML_Proc.evaluate, args=((True if len(pcapfile) == 1 else False),))
      ML_EV_PP.daemon = True
      ML_EV_PP.start()
      self.Procs.append(ML_EV_PP)
      if self.log_level >= vrb.INFO:
        self.logger.info('ML Analyze mode started!')

    if daemon or ( len(pcapfile) == 2 and pcapfile[1] ):
      if self.log_level >= vrb.INFO:
        self.logger.info('waiting for processing packets..')
      while not NSD_Packets_Queue.empty():
        time.sleep(2)

    time.sleep(2)
    while self.Sync_Queue.empty():
      if self.Sync_Queue.get() == 'KILL':
        self.logger.info('KILL')
        if self.log_level >= vrb.INFO and not daemon:
          self.logger.info('FINISHED! Killing all process..')
        elif daemon:
          self.logger.error('something was wrong! Killing all processes..')
        for proc in self.Procs:
          proc.terminate()
          proc.join(timeout=1.0)
        if self.log_level >= vrb.INFO:
          self.logger.info('DONE!')
        self.Mon_Proc.show_last_report(True)

    sys.excepthook = self.except_hook
