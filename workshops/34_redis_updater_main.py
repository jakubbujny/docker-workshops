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


#we need cache update here
