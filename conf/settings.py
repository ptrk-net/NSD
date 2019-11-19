# Config file

# Import libraries
import os

BASE_DIR = os.path.dirname('.')

# TEMPORAL DATABASE
TEMPORAL_DB_SERVER = '127.0.0.1'
TEMPORAL_DB_PORT = '27017'

# AFTER-PROCESSING DATABASE


# NETWORK
NETWORK_INTERFACE = 'enp0s25'
PROTOCOLS_FILE = BASE_DIR + 'Protocols'

# QUEUE
TCP_NUMBER_PROCESS = 10
UDP_NUMBER_PROCESS = 2
ICMP_NUMBER_PROCESS = 1

# LOGGING
LOGGING_LEVEL = 'DEBUG'
LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOGGING_FILE = BASE_DIR + '../logging/NSD_log.log'
