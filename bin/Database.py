# Database class

# Imports python libraries
from pymongo import MongoClient, errors
from bson import ObjectId
from datetime import datetime
import sys
import logging

# Import local libraries
from conf import variables as vrb
from conf.settings import DB_PCAP


# Class to manage the app's db
class Database:

  # Init method
  def __init__(self, log_level, db_server, db_port, db_name, sync_queue):
    self.log_level = log_level
    self.logger = logging.getLogger(__name__)
    self.SQ = sync_queue
    self.db_name = db_name

    if self.log_level >= vrb.INFO:
      self.logger.info('Accessing database..')
    try:
      self.client = MongoClient(db_server, db_port)
      self.db = self.client[self.db_name]
      if self.log_level >= vrb.DEBUG:
        self.logger.debug(self.db)
    except errors as err:
      self.logger.error('Error with database: {}'.format(err))
      self.SQ.put('KILL')

    if self.log_level >= vrb.INFO:
      self.logger.info('Database ready!')

  # Insert ICMP packets into the memory database
  def Database_insert_ICMP_packet(self, pkt):
    self.db.ICMP.insert_one(
      {
        'Date': datetime.now().strftime('%d/%m/%Y %H:%M:%S.%f'),
        'Source_IP': pkt[0],
        'Dest_IP': pkt[1],
        'Type': pkt[2],
        'Code': pkt[3],
        'Checksum': pkt[4],
        'Header': pkt[5],
        'Payload': str(pkt[6]),
        'cc': pkt[7]
      }
    )

  # Insert TCP packets into the memory database
  def Database_insert_TCP_packet(self, pkt):
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
        'Data': pkt[10],
        'cc': pkt[11]
      }
    )

  # Insert UDP packets into the memory database
  def Database_insert_UDP_packet(self, pkt):
    self.db.UDP.insert_one(
      {
        'Date': datetime.now().strftime('%d/%m/%Y %H:%M:%S.%f'),
        'Source_IP': pkt[0],
        'Dest_IP': pkt[1],
        'Source_Port': pkt[2],
        'Dest_Port': pkt[3],
        'Length': pkt[4],
        'Checksum': pkt[5],
        'UDP_type': pkt[6],
        'Data': pkt[7],
        'cc': pkt[8]
      }
    )

  # Reading memory database
  def Database_get_ICMP_packets(self):
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

  def Database_get_TCP_packets(self):
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

  def Database_get_UDP_flows_id(self, tagged):
    if tagged:
      aggregate_query = [
        {'$match': {'$or': [{'cc': 1}, {'cc': 0}]}},
        {'$group': {'_id': {'Source_IP': '$Source_IP', 'Dest_IP': '$Dest_IP'}}}
      ]
    else:
      aggregate_query = [
        {'$match': {'cc': 2}},
        {'$group': {'_id': {'Source_IP': '$Source_IP', 'Dest_IP': '$Dest_IP'}}}
      ]

    flows = list(self.db.UDP.aggregate(aggregate_query))
    packets = []
    for flow in flows:
      find_query = {
        'Source_IP': flow['_id']['Source_IP'],
        'Dest_IP': flow['_id']['Dest_IP']
      }
      get_id = {'_id': 1, 'cc': 1}
      packets.append(list(self.db.UDP.find(find_query, get_id).sort('Date').limit(1)))
    return packets

  def Database_get_TCP_flows_id(self, tagged):
    if tagged:
      aggregate_query = [
        {'$match': {'$or': [{'cc': 1}, {'cc': 0}]}},
        {'$group': {'_id': {'Source_IP': '$Source_IP', 'Source_Port': '$Source_Port',
                            'Dest_IP': '$Dest_IP', 'Dest_Port': '$Dest_Port'}}}
      ]
    else:
      aggregate_query = [
        {'$match': {'cc': 2}},
        {'$group': {'_id': {'Source_IP': '$Source_IP', 'Source_Port': '$Source_Port',
                            'Dest_IP': '$Dest_IP', 'Dest_Port': '$Dest_Port'}}}
      ]

    flows = list(self.db.TCP.aggregate(aggregate_query))
    packets = []
    for flow in flows:
      find_query = {
        'Source_IP': flow['_id']['Source_IP'],
        'Source_Port': flow['_id']['Source_Port'],
        'Dest_IP': flow['_id']['Dest_IP'],
        'Dest_Port': flow['_id']['Dest_Port']
      }
      get_id = {'_id': 1, 'cc': 1}
      packets.append(list(self.db.TCP.find(find_query, get_id).sort('Date').limit(1)))
    return packets

  def Database_get_ICMP_flows_id(self, tagged):
    if tagged:
      aggregate_query = [
        {'$match': {'$or': [{'cc': 1}, {'cc': 0}]}},
        {'$group': {'_id': {'Source_IP': '$Source_IP', 'Dest_IP': '$Dest_IP'}}}
      ]
    else:
      aggregate_query = [
        {'$match': {'cc': 2}},
        {'$group': {'_id': {'Source_IP': '$Source_IP', 'Dest_IP': '$Dest_IP'}}}
      ]

    flows = list(self.db.ICMP.aggregate(aggregate_query))
    packets = []
    for flow in flows:
      find_query = {
        'Source_IP': flow['_id']['Source_IP'],
        'Dest_IP': flow['_id']['Dest_IP'],
      }
      get_id = {'_id': 1, 'cc': 1}
      packets.append(list(self.db.ICMP.find(find_query, get_id).sort('Date').limit(1)))
    return packets

  def Database_get_RTP_flows_id(self, tagged):
    if self.db_name == DB_PCAP:
      if tagged:
        aggregate_query = [
          {'$match': {'$or': [{'cc': 1}, {'cc': 0}]}},
          {'$group': {'_id': {'Source_IP': '$Source_IP', 'Dest_IP': '$Dest_IP'}}}
        ]
      else:
        aggregate_query = [
          {'$match': {'cc': 2}},
          {'$group': {'_id': {'Source_IP': '$Source_IP', 'Dest_IP': '$Dest_IP'}}}
        ]
    else:
      if tagged:
        aggregate_query = [
          {'$match': {'$and': [{'$or': [{'UDP_type': 0}, {'UDP_type': 196}]}, {'$or': [{'cc': 1}, {'cc': 0}]}]}},
          {'$group': {'_id': {'Source_IP': '$Source_IP', 'Dest_IP': '$Dest_IP'}}}
        ]
      else:
        aggregate_query = [
          {'$match': {'$and': [{'UDP_type': 0}, {'cc': 2}]}},
          {'$match': {'$and': [{'$or': [{'UDP_type': 0}, {'UDP_type': 196}]}, {'cc': 2}]}},
          {'$group': {'_id': {'Source_IP': '$Source_IP', 'Dest_IP': '$Dest_IP'}}}
        ]

    flows = list(self.db.UDP.aggregate(aggregate_query))
    packets = []
    for flow in flows:
      find_query = {
        'Source_IP': flow['_id']['Source_IP'],
        'Dest_IP': flow['_id']['Dest_IP'],
      }
      get_id = {'_id': 1, 'cc': 1}
      packets.append(list(self.db.UDP.find(find_query, get_id).sort('Date').limit(1)))
    return packets

  def Database_get_RTP_traffic_by_id(self, id):
    IPs = list(self.db.UDP.find({'_id': ObjectId(id)}, {'Source_IP': 1, 'Dest_IP': 1, '_id': 0}))
    return list(self.db.UDP.find(
      {'Source_IP': IPs[0]['Source_IP'], 'Dest_IP': IPs[0]['Dest_IP']},
      {'Data': 1, '_id': 0}).sort('Date')
                )

  def Database_get_RTP_identification_by_id(self, id):
    IP = self.db.UDP.find({'_id': ObjectId(id)}, {'Source_IP': 1, 'Dest_IP': 1, '_id': 0})
    return [IP[0]['Source_IP'], IP[0]['Dest_IP']]

  def Database_drop_database(self):
    if self.db_name == DB_PCAP:
      self.db.command('dropDatabase')
