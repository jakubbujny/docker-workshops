import pika
import json
import os
import sys
import time
from pymongo import MongoClient
import flask
import pprint
import redis

#We need redis connection here
redisConnection = None
while redisConnection is None:
   time.sleep(1)
   try:
     redisConnection = redis.StrictRedis(host='redis', port=6379, db=0)
   except:
      print("Error in connection to redis")
      sys.stdout.flush()

#we need mongo connection here
mongoConnection = None
while mongoConnection is None:
   time.sleep(1)
   try:
      mongoConnection = MongoClient('mongo', 27017)
   except:
      print("Error in connection to mongo")
      sys.stdout.flush()


#we need cache update here
while True:
   time.sleep(1)
   pipeline = [{ "$group": {"_id":"$group", "average": { "$avg": "$speed" }}}]
   resultList = list(mongoConnection.cars.incoming.aggregate(pipeline))
   sys.stdout.flush()
   for averageObject in resultList:
      redisConnection.set('group_average_speed_'+str(averageObject['_id']), averageObject['average'])
