import time  
import pika
import random
import json
import datetime
import sys
import os

MAX_SPEED = 40 # m/s
MIN_SPEED = 10 # m/s


#We need some ID here
hostname = os.environ['HOSTNAME']
id = 0
for c in hostname:
    id += ord(c)

    print("Starting with id: "+str(id))


#We need some group here

#We need some random state here


#We need some queue connection here


while True:
    # We need to calculate current state here

    # We need to randomize state for next iteration

    #We need some message publish herea


    time.sleep(0.1)

