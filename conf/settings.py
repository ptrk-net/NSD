# Config file

# Import libraries
import os

BASE_DIR = os.path.dirname('.')

# DATABASE
DB_SERVER = '127.0.0.1'
DB_PORT = 27017
DB_NAME = 'NSD_db'
DB_PCAP = 'NSD_pcap_db'

# NETWORK
NETWORK_INTERFACE = 'enp7s0'

# PROCESSES
TCP_NUMBER_PROCESS = 10
UDP_NUMBER_PROCESS = 5
ICMP_NUMBER_PROCESS = 1

# LOGGING
LOGGING_LEVEL = 0
LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOGGING_FILE = BASE_DIR + 'logging/detector.log'

# MACHINE LEARNING
FEATURES = 100
T = 3
S = 2
CLF = BASE_DIR + 'dump/classifier.dump'
CLF_MCC = BASE_DIR + 'dump/clf_mcc'
TRAINING_ITERATIONS = 20
