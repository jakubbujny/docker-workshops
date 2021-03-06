import time  
import pika
import random
import json
import datetime
import sys
import os

MAX_SPEED = 40 # m/s
MIN_SPEED = 10 # m/s

hostname = os.environ['HOSTNAME']
id = 0

for c in hostname:
   id += ord(c)

print("Starting with id: "+str(id))

group = random.randint(1,3)

random.seed(id)
currentSpeed = random.randint(10,40)
currentFuel = 600000
currentFuelUsage = int(currentSpeed/10)

def randomizeState():
   global currentSpeed
   speedUpOrSlowDown = 1
   if currentSpeed == MAX_SPEED:
      speedUpOrSlowDown = 0
   elif currentSpeed == MIN_SPEED:
      speedUpOrSlowDown = 1
   else:
      speedUpOrSlowDown = random.randint(0,1)

   if speedUpOrSlowDown == 1:
      currentSpeed += 1
   else:
      currentSpeed -= 1

def calculateState():
   global currentFuel
   global currentFuelUsage
   currentFuel -= (currentFuelUsage/10)
   currentFuelUsage = int(currentSpeed/10)

rabbitConnection = None

while rabbitConnection is None:
   time.sleep(1)
   try:
      rabbitConnection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
   except:
      print("Error in connection")
      sys.stdout.flush()

channel = rabbitConnection.channel()
channel.exchange_declare(exchange='incoming',
                         exchange_type='fanout')
while True:
    sys.stdout.flush()
    calculateState()
    randomizeState()
    body = json.dumps({
        'speed' : currentSpeed,
        'fuel' : currentFuel,
        'fuelUsage': currentFuelUsage,
        'id' : id,
        'group' : group,
        'timestamp' : int(datetime.datetime.now().timestamp())
    })
    channel.basic_publish(exchange='incoming',
                      routing_key='',
                      body=body)
   
    time.sleep(0.1)

conn.disconnect()
