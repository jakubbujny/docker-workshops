import pika
import json
import os
import sys
import time
from pymongo import MongoClient
import flask
import pprint

hostname = os.environ['HOSTNAME']
id = 0

for c in hostname:
   id += ord(c)

mongoConnection = None
while mongoConnection is None:
   time.sleep(1)
   try:
      mongoConnection = MongoClient('mongo', 27017)
   except:
      print("Error in connection to mongo")
      sys.stdout.flush()


app = flask.Flask(__name__)

@app.route('/average-speed-group/<groupId>')
def getAverageSpeedForGroup(groupId):
   global mongoConnection
   pipeline = [{ "$match": {"group" : int(groupId) }},{ "$group": {"_id": None,"average": { "$avg": "$speed" }}}]
   result = list(mongoConnection.cars.incoming.aggregate(pipeline))[0]['average']
   return str(result)

app.run(host='0.0.0.0', port=80, threaded = True)
