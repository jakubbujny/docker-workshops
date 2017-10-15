import pika
import json
import os
import sys
import time
from pymongo import MongoClient
import flask
import pprint
import uuid
import pika
import traceback
import redis

hostname = os.environ['HOSTNAME']
id = 0

for c in hostname:
   id += ord(c)

redisConnection = None
while redisConnection is None:
   time.sleep(1)
   try:
      redisConnection = redis.StrictRedis(host='redis', port=6379, db=0)
   except:
      print("Error in connection to redis")
      sys.stderr.flush()
      sys.stdout.flush()

mongoConnection = None
while mongoConnection is None:
   time.sleep(1)
   try:
      mongoConnection = MongoClient('mongo', 27017)
   except:
      print("Error in connection to mongo")
      sys.stdout.flush()

rabbitConnection = None

while rabbitConnection is None:
    time.sleep(1)
    try:
        rabbitConnection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    except:
        print("Error in connection to rabbit")
        sys.stdout.flush()

channel = rabbitConnection.channel()
channel.queue_declare(queue='report_queue', durable=True)

def callback(ch, method, properties, body):
    bodyMap = json.loads(body)
    values = list(mongoConnection.cars.incoming.find({"id": int(bodyMap['id'])}))
    sum = 0
    for value in values:
        sum += value['speed'] * 0.1
    redisConnection.incrbyfloat(bodyMap['taskId']+"_result", sum)
    redisConnection.decr(bodyMap['taskId'])
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='report_queue')

channel.start_consuming()
