import time  
import stomp
import random
import json
import datetime

MAX_SPEED = 40
MIN_SPEED = 5

MAX_FUEL_USAGE = 20
MIX_FUEL_USAGE = 3

currentSpeed = 10
currentFuel = 60
currentFuelUsage = 5
random.seed(5)
id = 1
group = 1
  
queueConn = stomp.Connection([('activemq', 61613)])
queueConn.start()
queueConn.connect('admin', 'password', wait=True)
while True:
    queueConn.send(body=json.dumps({
        'speed' : currentSpeed,
        'fuel' : currentFuel,
        'fuelUsage': currentFuelUsage,
        'id' : id,
        'group' : group,
        'timestamp' : datetime.datetime.now().timestamp()
    }), destination='/queue/test')

    time.sleep(2)

conn.disconnect()
