# Database class

# Imports python libraries
from pymongo import MongoClient
from datetime import datetime
import logging


# Class to manage the app's db
class NSD_Database:
	
	# Init method
	def __init__(self, db_server, db_port, sync_queue):
		self.logger = logging.getLogger(__name__)
		self.SQ = sync_queue
		self.client = MongoClient(db_server, db_port)
		self.db = self.client.NSD_database
		#try:
		#except Error as error:
		#	print('Error creating database: ' + error.args[0])
		#	self.SQ.put('KILL')
		#	sys.exit()

	# Insert TCP packets into the memory database
	def NSD_Database_insert_TCP_packet(self, pkt):
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
		self.db.UDP.insert_one(
			{
				'Date': datetime.now().strftime('%d/%m/%Y %H:%M:%S.%f'),
				'Source_IP': pkt[0],
				'Dest_IP': pkt[1],
				'Type': pkt[2],
				'Code': pkt[3],
			}
		)

