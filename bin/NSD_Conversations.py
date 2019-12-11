# Import python libraries
import logging

# Import NSD libraries
from bin.NSD_Database import NSD_Database
from conf import settings as cfg

class NSD_Conversations:

    def __init__(self, log_level, db_server, db_port, counters, sync_queue):
        self.log_level = log_level
        self.logger = logging.getLogger(__name__)
        self.Counters = counters
        self.SQ = sync_queue
        self.db_server = db_server
        self.db_port = db_port

    def NSD_Conversations_fork_database(self):
        self.DB = NSD_Database(self.log_level, self.db_server, self.db_port, self.SQ)  # MongoDB

    def NSD_Conversations_flow_ICMP(self):
        self.NSD_Conversations_fork_database(self)

        if self.log_level == 'DEBUG':
            self.logger.debug('NSD_Conversations_flow_ICMP: reading..')

        group = {}
        self.DB.NSD_Database_get_ICMP_packets(group)

        # TODO
        # 1. parser response
        # 2. check local dict conversations db
        # 3. if exists, update counters with conversation_id
        # 4. if does not exist, create conversation_id and update counter

