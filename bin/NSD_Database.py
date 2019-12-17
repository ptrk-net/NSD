# Database class

# Imports python libraries
from pymongo import MongoClient
from datetime import datetime
import sys
import logging


# Class to manage the app's db
class NSD_Database:

    # Init method
    def __init__(self, log_level, db_server, db_port, sync_queue):
        self.log_level = log_level
        self.logger = logging.getLogger(__name__)
        self.SQ = sync_queue
        self.logger.info('Accessing database..')
        try:
            self.client = MongoClient(db_server, db_port)
            self.db = self.client['NSD_db']
        except:
            self.logger.error('Error with database: {0}'.format(sys.exc_info()[0]))
            self.SQ.put('KILL')
        # raise ConnectionError('Error with database: {0}'.format(sys.exc_info()[0]))
        # sys.exit()
        self.logger.info('Database ready!')

    # Insert ICMP packets into the memory database
    def NSD_Database_insert_ICMP_packet(self, pkt):
        self.db.ICMP.insert_one(
            {
                'Date': datetime.now().strftime('%d/%m/%Y %H:%M:%S.%f'),
                'Source_IP': pkt[0],
                'Dest_IP': pkt[1],
                'Type': pkt[2],
                'Code': pkt[3],
                'Checksum': pkt[4],
                'Header': pkt[5],
                'Payload': pkt[6]
            }
        )

    # Insert TCP packets into the memory database
    def NSD_Database_insert_TCP_packet(self, pkt):
        if self.log_level == 'DEBUG':
            self.logger.debug('NSD_Database_insert_TCP_packet: inserting..')
        self.db.TCP.insert_one(
            {
                'Date': datetime.now().strftime('%d/%m/%Y %H:%M:%S.%f'),
                'Source_IP': pkt[0],
                'Dest_IP': pkt[1],
                'Source_Port': pkt[2],
                'Dest_Port': pkt[3],
                'Sequence_Number': pkt[4],
                'ACK_Number': pkt[5],
                'Flags': pkt[6],
                'Window': pkt[7],
                'Checksum': pkt[8],
                'Urgent_Pointer': pkt[9],
                'Data': pkt[10]
            }
        )

    # Insert UDP packets into the memory database
    def NSD_Database_insert_UDP_packet(self, pkt):
        self.db.UDP.insert_one(
            {
                'Date': datetime.now().strftime('%d/%m/%Y %H:%M:%S.%f'),
                'Source_IP': pkt[0],
                'Dest_IP': pkt[1],
                'Source_Port': pkt[2],
                'Dest_Port': pkt[3],
                'Length': pkt[4],
                'Checksum': pkt[5],
                'Data': pkt[6]
            }
        )

    # Reading memory database
    def NSD_Database_get_ICMP_packets(self):
        aggregate_query = [{
            '$group': {
                '_id': {
                    'Source_IP': '$Source_IP',
                    'Dest_IP': '$Dest_IP'
                }
            }
        }]
        packets = []
        flows = list(self.db.ICMP.aggregate(aggregate_query))
        for flow in flows:
            find_query = {
                'Source_IP': flow['_id']['Source_IP'],
                'Dest_IP': flow['_id']['Dest_IP']
            }
            packets.append(list(self.db.ICMP.find(find_query)))
        return packets

    def NSD_Database_get_TCP_packets(self):
        aggregate_query = [{
            '$group': {
                '_id': {
                    'Source_IP': '$Source_IP',
                    'Source_Port': '$Source_Port',
                    'Dest_IP': '$Dest_IP',
                    'Dest_Port': '$Dest_Port'
                }
            }
        }]
        packets = []
        flows = list(self.db.TCP.aggregate(aggregate_query))
        for flow in flows:
            find_query = {
                'Source_IP': flow['_id']['Source_IP'],
                'Source_Port': flow['_id']['Source_Port'],
                'Dest_IP': flow['_id']['Dest_IP'],
                'Dest_Port': flow['_id']['Dest_Port']
            }
            packets.append(list(self.db.TCP.find(find_query)))
        return packets

    def NSD_Database_get_UDP_packets(self):
        aggregate_query = [{
            '$group': {
                '_id': {
                    'Source_IP': '$Source_IP',
                    'Source_Port': '$Source_Port',
                    'Dest_IP': '$Dest_IP',
                    'Dest_Port': '$Dest_Port'
                }
            }
        }]
        packets = []
        flows = list(self.db.UDP.aggregate(aggregate_query))
        for flow in flows:
            find_query = {
                'Source_IP': flow['_id']['Source_IP'],
                'Source_Port': flow['_id']['Source_Port'],
                'Dest_IP': flow['_id']['Dest_IP'],
                'Dest_Port': flow['_id']['Dest_Port']
            }
            packets.append(list(self.db.UDP.find(find_query)))
        return packets
