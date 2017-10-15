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




app = flask.Flask(__name__)

def publishTasksToRabbit(taskId, idsList):
    rabbitConnection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))

    channel = rabbitConnection.channel()
    channel.queue_declare(queue='report_queue', durable=True)
    for id in idsList:
        taskToPublish = {"taskId": taskId, "id" : id}
        channel.basic_publish(exchange='',
                              routing_key='report_queue',
                              body=json.dumps(taskToPublish),
                              properties=pika.BasicProperties(
                                  delivery_mode = 2, # make message persistent
                              ))
    rabbitConnection.close()

@app.route('/report-group-distance/<groupId>')
def reportDistance(groupId):
   global mongoConnection
   global redisConnection


   UUID = str(uuid.uuid4())

   idsList = list(mongoConnection.cars.incoming.find({"group": int(groupId)}).distinct("id"))

   print(idsList)
   sys.stdout.flush()

   redisConnection.set(UUID, len(idsList))
   publishTasksToRabbit(taskId=UUID, idsList=idsList)

   while int(redisConnection.get(UUID)) > 0:
       time.sleep(0.1)

   redisConnection.delete(UUID)
   toReturn = redisConnection.get(UUID+"_result")
   redisConnection.delete(UUID+"_result")
   return str(toReturn)

app.run(host='0.0.0.0', port=80, threaded = True)
