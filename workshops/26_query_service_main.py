import pika
import json
import os
import sys
import time
from pymongo import MongoClient
import flask
import pprint


#We need mongo connection here
mongoConnection = None
while mongoConnection is None:
   time.sleep(1)
   try:
      mongoConnection = MongoClient('mongo', 27017)
   except:
      print("Error in connection to mongo")
      sys.stdout.flush()


#We need query endpoint here 
