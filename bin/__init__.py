# Logging

# Imports python libraries
import logging.config
from os import path, remove

# Imports local libraries
from conf import settings as cfg
from .Monitor import Monitor_Data
from .Database import Database
from .Init import Init
from .Monitor import Monitor
from .Network import Network
from .Packets_Queue import Packets_Queue
from .Pcap import Pcap
from .Processor import Processor
from .Machine_Learning import Machine_Learning

# If applicable, delete the existing log file to generate a fresh log file during each execution
if path.isfile(cfg.LOGGING_FILE):
  remove(cfg.LOGGING_FILE)

# Create the Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a Formatter for formatting the log messages
logger_formatter = logging.Formatter(cfg.LOGGING_FORMAT)

# Create the Handler for logging data to a file
logger_fh = logging.FileHandler(cfg.LOGGING_FILE)
logger_fh.setLevel(logging.DEBUG)

# Add the Formatter to the Handler
logger_fh.setFormatter(logger_formatter)

# Create the Handler for logging data to console
logger_sh = logging.StreamHandler()
logger_sh.setLevel(logging.DEBUG)

# Add the Formatter to the Handler
logger_sh.setFormatter(logger_formatter)

# Add the Handlers to the Logger
logger.addHandler(logger_fh)
logger.addHandler(logger_sh)
# logger.info('Completed configuring logger()!')
