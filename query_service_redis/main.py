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


app = flask.Flask(__name__)

@app.route('/average-speed-group/<groupId>')
def getAverageSpeedForGroup(groupId):
   result = redisConnection.get('group_average_speed_'+groupId)
   return result


app.run(host='0.0.0.0', port=80, threaded = True)
