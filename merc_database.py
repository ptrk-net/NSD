import sqlite3

class Merc_Database:
	
	# Init method
	def __init__(self, memory, sync_queue):
		self.SQ = sync_queue
		database = 'file::memory:?cache=shared' if memory else 'file:/opt/Merc/__db__/merc_packets_db.db'
		try:
			self.db = sqlite3.connect( database )
			self.cursor = self.db.cursor()
			Merc_Database.merc_database_init_inMemory(self) if memory else merc_database_init_inFile(self)
		except sqlite3.Error as error:
			print('Error creating database: ' + error.args[0])
			self.SQ.put('KILL')

	# Init in-memory database
	def merc_database_init_inMemory(self):
		Merc_Database.merc_database_execute(self,'CREATE TABLE IF NOT EXISTS TCP(Source_IP TEXT, Dest_IP TEXT, Source_Port TEXT, Dest_Port TEXT, Sequence_Number INT, ACK_Number INT, Date TEXT, Data TEXT)')
		Merc_Database.merc_database_execute(self,'CREATE TABLE IF NOT EXISTS UDP(Source_IP TEXT, Dest_IP TEXT, Source_Port TEXT, Dest_Port TEXT, Date TEXT, Data TEXT)')
		Merc_Database.merc_database_execute(self,'CREATE TABLE IF NOT EXISTS ICMP(Source_IP TEXT, Dest_IP TEXT, Type INT, Code INT)')
		Merc_Database.merc_database_commit(self)
		

	# Execute statement
	def merc_database_execute(self, statement):
		try:
			return self.cursor.execute(statement)
		except sqlite3.Error as error:
			self.db.rollback()
			print('Error creating database: ' + error.args[0])
			self.SQ.put('KILL')

	# Commit
	def merc_database_commit(self):
		self.db.commit()

	# Close
	def merc_database_close(self):
		self.db.close()

	# Insert TCP packets into database
	def merc_database_insert_TCP_packet(self, pkt):
		statement = 'INSERT INTO TCP VALUES('  + \
			'Date="' + pkt[0] + '", ' + \
			'Source_IP="' + pkt[1] + '", ' + \
			'Dest_IP="' + pkt[2] + '", ' + \
			'Source_Port="' + str(pkt[3]) + '", ' + \
			'Dest_Port="' + str(pkt[4]) + '", ' + \
			'Sequence_Number=' + str(pkt[5]) + ', ' + \
			'ACK_Number=' + str(pkt[6]) + ', ' + \
			'Data="' + pkt[7] + '" ' + \
			');'
		#print('* ICMP: ' + str(pkt[8]))
		#print(statement)
		self.SQ.put('KILL')
		#merc_database_execute(self, statement) 

	# Insert TCP packets into database
	def merc_database_insert_UDP_packet(self, pkt):
		statement = 'INSERT INTO UDP VALUES('  + \
			'Date="' + pkt[0] + '", ' + \
			'Source_IP="' + pkt[1] + '", ' + \
			'Dest_IP="' + pkt[2] + '", ' + \
			'Source_Port="' + str(pkt[3]) + '", ' + \
			'Dest_Port="' + str(pkt[4]) + '", ' + \
			'Data="' + pkt[5] + '" ' + \
			');'
		#rint('* ICMP: ' + str(pkt[6]))
		#print(statement)
		self.SQ.put('KILL')
		#merc_database_execute(self, statement) 

	# Insert TCP packets into database
	def merc_database_insert_ICMP_packet(self, pkt):
		statement = 'INSERT INTO ICMP VALUES('  + \
			'Date="' + pkt[0] + '", ' + \
			'Source_IP="' + pkt[1] + '", ' + \
			'Dest_IP="' + pkt[2] + '", ' + \
			'Type=' + str(pkt[3]) + ', ' + \
			'Code=' + str(pkt[4]) + \
			');'
		#print('* ICMP: ' + str(pkt[5]))
		#print(statement)
		self.SQ.put('KILL')
		#merc_database_execute(self, statement) 

