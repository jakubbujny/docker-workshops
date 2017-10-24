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

#Exchange and bounded queue here

#Callback saving to mongo 
