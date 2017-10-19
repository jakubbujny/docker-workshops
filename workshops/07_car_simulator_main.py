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
group = random.randint(1,3)

#We need some random state here
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


#We need some queue connection here


while True:
    # We need to calculate current state here

    # We need to randomize state for next iteration

    #We need some message publish herea


    time.sleep(0.1)

