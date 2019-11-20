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
			#raise ConnectionError('Error with database: {0}'.format(sys.exc_info()[0]))
		#	sys.exit()
		self.logger.info('Database ready!')

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
				'Data': pkt[6]
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
				'Data': pkt[4]
			}
		)

	# Insert ICMP packets into the memory database
	def NSD_Database_insert_ICMP_packet(self, pkt):
		self.db.ICMP.insert_one(
			{
				'Date': datetime.now().strftime('%d/%m/%Y %H:%M:%S.%f'),
				'Source_IP': pkt[0],
				'Dest_IP': pkt[1],
				'Type': pkt[2],
				'Code': pkt[3],
			}
		)

