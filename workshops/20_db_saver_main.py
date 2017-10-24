import pika
import json
import os
import sys
import time
from pymongo import MongoClient

#We need rabbit connection here
rabbitConnection = None

while rabbitConnection is None:
   time.sleep(1)
   try:
      rabbitConnection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
   except:
      print("Error in connection to rabbit")
      sys.stdout.flush()

#We need mongo connection here
mongoConnection = None
while mongoConnection is None:
   time.sleep(1)
   try:
      mongoConnection = MongoClient('mongo', 27017)
   except:
      print("Error in connection to mongo")
      sys.stdout.flush()

#Exchange and bounded queue here
channel = rabbitConnection.channel()
channel.exchange_declare(exchange='incoming',
                         exchange_type='fanout')

queue_name = 'db_saver'
result = channel.queue_declare(queue=queue_name, exclusive=False)

channel.queue_bind(exchange='incoming',
                   queue=queue_name)

#Callback saving to mongo 
