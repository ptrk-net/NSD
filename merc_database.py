# system libraries
import sqlite3
import sys
from datetime import datetime

# Class to manage the app's db
class Merc_Database:
	
	# Init method
	def __init__(self, memory, sync_queue):
		self.SQ = sync_queue
		database = 'file::memory:?cache=shared' if memory else 'file:/opt/Merc/__db__/merc_packets_db.db'
		try:
			self.db = sqlite3.connect(database)
			self.cursor = self.db.cursor()
			Merc_Database.merc_database_init_inMemory(self) if memory else Merc_Database.merc_database_init_inFile(self)
		except sqlite3.Error as error:
			print('Error creating database: ' + error.args[0])
			self.SQ.put('KILL')
			sys.exit()

	# Init in-memory database
	def merc_database_init_inMemory(self):
		print('Creating Database in memory...')
		Merc_Database.merc_database_execute(self,'CREATE TABLE IF NOT EXISTS TCP(Source_IP TEXT, Dest_IP TEXT, Source_Port INT, Dest_Port INT, Sequence_Number INT, ACK_Number INT, Date TEXT, Data TEXT);')
		Merc_Database.merc_database_execute(self,'CREATE TABLE IF NOT EXISTS UDP(Source_IP TEXT, Dest_IP TEXT, Source_Port INT, Dest_Port INT, Date TEXT, Data TEXT);')
		Merc_Database.merc_database_execute(self,'CREATE TABLE IF NOT EXISTS ICMP(Source_IP TEXT, Dest_IP TEXT, Type INT, Code INT, Date TEXT);')
		Merc_Database.merc_database_commit(self)
		#for row in self.cursor.execute('pragma table_info(UDP);'):
		#	print(row)

		
	# Init  database
	def merc_database_init_inFile(self):
		Merc_Database.merc_database_execute(self,'CREATE TABLE IF NOT EXISTS TCP(Source_IP TEXT, Dest_IP TEXT, Source_Port INT, Dest_Port INT, Last_Sequence_Number INT, Last_ACK_Number INT, Initial_Date TEXT, Final_Date TEXT, Total_Bytes INT, Conversation INT);')
		Merc_Database.merc_database_execute(self,'CREATE TABLE IF NOT EXISTS UDP(Source_IP TEXT, Dest_IP TEXT, Source_Port INT, Dest_Port INT, Initial_Date TEXT, Final_Date TEXT, Total_Bytes INT, Conversation INT);')
		Merc_Database.merc_database_execute(self,'CREATE TABLE IF NOT EXISTS ICMP(Source_IP TEXT, Dest_IP TEXT, Type INT, Code INT, Number_Packets INT, Conversation INT);')
		Merc_Database.merc_database_commit(self)

	# Execute statement
	def merc_database_execute(self, statement):
		try:
			return self.cursor.execute(statement)
		except sqlite3.Error as error:
			self.db.rollback()
			print('Error executing statement: ' + error.args[0] + ': ' + statement)
			self.SQ.put('KILL')

	# Commit
	def merc_database_commit(self):
		self.db.commit()

	# Close
	def merc_database_close(self):
		self.db.close()

	# Insert TCP packets into the memory database
	def merc_database_insert_TCP_packet_inMemory(self, pkt):
		Date = datetime.now().strftime('%d/%m/%Y %H:%M:%S.%f')
		statement = 'INSERT INTO TCP ' + \
			'(Date, Source_IP, Dest_IP, Source_Port, Dest_Port, Sequence_Number, ACK_Number, Data) ' + \
			'VALUES ('  + \
			'"' + Date + '", ' + \
			'"' + pkt[0] + '", ' + \
			'"' + pkt[1] + '", ' + \
			str(pkt[2]) + ', ' + \
			str(pkt[3]) + ', ' + \
			str(pkt[4]) + ', ' + \
			str(pkt[5]) + ', ' + \
			'"' + str(pkt[6]) + '"' + \
			');'
		#print(statement)
		#self.SQ.put('KILL')
		Merc_Database.merc_database_execute(self, statement) 
		Merc_Database.merc_database_commit(self)

	# Insert UDP packets into the memory database
	def merc_database_insert_UDP_packet_inMemory(self, pkt):

		Date = datetime.now().strftime('%d/%m/%Y %H:%M:%S.%f')
		statement = 'INSERT INTO UDP ' + \
			'(Date, Source_IP, Dest_IP, Source_Port, Dest_Port, Data) ' + \
			'VALUES ('  + \
			'"' + Date + '", ' + \
			'"' + pkt[0] + '", ' + \
			'"' + pkt[1] + '", ' + \
			str(pkt[2]) + ', ' + \
			str(pkt[3]) + ', ' + \
			'"' + pkt[4] + '"' + \
			');'
		#print(statement)
		#self.SQ.put('KILL')
		Merc_Database.merc_database_execute(self, statement) 
		Merc_Database.merc_database_commit(self)

	# Insert ICMP packets into the memory database
	def merc_database_insert_ICMP_packet_inMemory(self, pkt):
		Date = datetime.now().strftime('%d/%m/%Y %H:%M:%S.%f')
		statement = 'INSERT INTO ICMP ' + \
			'(Date, Source_IP, Dest_IP, Type, Code) ' + \
			'VALUES ('  + \
			'"' + Date + '", ' + \
			'"' + pkt[0] + '", ' + \
			'"' + pkt[1] + '", ' + \
			str(pkt[2]) + ', ' + \
			str(pkt[3]) + \
			');'
		#print(statement)
		#self.SQ.put('KILL')
		Merc_Database.merc_database_execute(self, statement) 
		Merc_Database.merc_database_commit(self)

	# Insert TCP packets into the memory database
	def merc_database_insert_TCP_packet_inFile(self, pkt, position):
		statement = 'INSERT INTO TCP VALUES('  + \
			'Conversation="' + pkt[0] + '", ' + \
			'Source_IP="' + pkt[1] + '", ' + \
			'Dest_IP="' + pkt[2] + '", ' + \
			'Source_Port=' + str(pkt[3]) + ', ' + \
			'Dest_Port=' + str(pkt[4]) + ', ' + \
			'Last_Sequence_Number=' + str(pkt[5]) + ', ' + \
			'Last_ACK_Number=' + str(pkt[6]) + ', ' + \
			'Total_Bytes=' + pkt[7]
		if position == 1:
			Date = datetime.now().strftime('%d/%m/%Y %H:%M:%S.%f')
			statement += ', Initial_Date="' + Date + '");'
		elif position == 2:
			Date = datetime.now().strftime('%d/%m/%Y %H:%M:%S.%f')
			statement += ', Final_Date="' + Date + '");'
		elif position == 0:
			statement += ');'
		#print(statement)
		#self.SQ.put('KILL')
		Merc_Database.merc_database_execute(self, statement) 
		Merc_Database.merc_database_commit(self)

	# Insert UDP packets into the memory database
	def merc_database_insert_UDP_packet_inFile(self, pkt, position):
		statement = 'INSERT INTO UDP VALUES('  + \
			'Conversation="' + pkt[0] + '", ' + \
			'Source_IP="' + pkt[1] + '", ' + \
			'Dest_IP="' + pkt[2] + '", ' + \
			'Source_Port="' + str(pkt[3]) + '", ' + \
			'Dest_Port="' + str(pkt[4]) + '", ' + \
			'Total_Bytes=' + pkt[5]
		if position == 1:
			Date = datetime.now().strftime('%d/%m/%Y %H:%M:%S.%f')
			statement += ', Initial_Date="' + Date + '");'
		elif position == 2:
			Date = datetime.now().strftime('%d/%m/%Y %H:%M:%S.%f')
			statement += ', Final_Date="' + Date + '");'
		elif position == 0:
			statement += ');'
		#print(statement)
		#self.SQ.put('KILL')
		Merc_Database.merc_database_execute(self, statement) 
		Merc_Database.merc_database_commit(self)

	# Insert ICMP packets into the memory database
	def merc_database_insert_ICMP_packet_inFile(self, pkt):
		statement = 'INSERT INTO ICMP VALUES('  + \
			'Conversation="' + pkt[0] + '", ' + \
			'Source_IP="' + pkt[1] + '", ' + \
			'Dest_IP="' + pkt[2] + '", ' + \
			'Type=' + str(pkt[3]) + ', ' + \
			'Code=' + str(pkt[4]) + \
			');'
		#print(statement)
		#self.SQ.put('KILL')
		Merc_Database.merc_database_execute(self, statement) 
		Merc_Database.merc_database_commit(self)

