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
def callback(ch, method, properties, body):
    global mongoConnection
    mongoConnection.cars.incoming.insert_one(json.loads(body))
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue=queue_name)

channel.start_consuming()

