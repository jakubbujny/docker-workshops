import pika
import json
import os
import sys
import time
from pymongo import MongoClient
import flask
import pprint
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
      sys.stdout.flush()

mongoConnection = None
while mongoConnection is None:
   time.sleep(1)
   try:
      mongoConnection = MongoClient('mongo', 27017)
   except:
      print("Error in connection to mongo")
      sys.stdout.flush()


while True:
   time.sleep(0.1)
   pipeline = [{ "$group": {"_id":"$group", "average": { "$avg": "$speed" }}}]
   resultList = list(mongoConnection.cars.incoming.aggregate(pipeline))
   sys.stdout.flush()
   for averageObject in resultList:
      redisConnection.set('group_average_speed_'+str(averageObject['_id']), averageObject['average'])
