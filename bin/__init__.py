# Logging

# Imports python libraries
import logging.config
from os import path, remove

# Imports NSD
from conf import settings as cfg
from .NSD_Counters import NSD_Counters
from .NSD_Database import NSD_Database
from .NSD_Main import NSD_Main
from .NSD_Monitor import NSD_Monitor
from .NSD_Network import NSD_Network
from .NSD_Packets_Queue import NSD_Packets_Queue
from .NSD_Pcap import NSD_Pcap
from .NSD_Process import NSD_Process


# If applicable, delete the existing log file to generate a fresh log file during each execution
if path.isfile(cfg.LOGGING_FILE):
    remove(cfg.LOGGING_FILE)

# Create the Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create the Handler for logging data to a file
logger_handler = logging.FileHandler(cfg.LOGGING_FILE)
logger_handler.setLevel(logging.DEBUG)

# Create a Formatter for formatting the log messages
logger_formatter = logging.Formatter(cfg.LOGGING_FORMAT)

# Add the Formatter to the Handler
logger_handler.setFormatter(logger_formatter)

# Add the Handler to the Logger
logger.addHandler(logger_handler)
logger.info('Completed configuring logger()!')

