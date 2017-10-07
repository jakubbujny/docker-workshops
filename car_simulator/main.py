import time  
import pika
import random
import json
import datetime
import sys

MAX_SPEED = 40
MIN_SPEED = 10

id = 1
group = random.randint(1,5)

random.seed(5)
currentSpeed = random.randint(10,40)
currentFuel = 60000
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
   currentFuel -= currentFuelUsage      
   currentFuelUsage = int(currentSpeed/10)


time.sleep(5)
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()
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
   
    print("message sent: "+body)
    time.sleep(1)

conn.disconnect()
