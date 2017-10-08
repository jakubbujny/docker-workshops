import pika
import json
import os
import sys
import time

hostname = os.environ['HOSTNAME']
id = 0

for c in hostname:
   id += ord(c)

connection = None

while connection is None:
   time.sleep(1)
   try:
      connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
   except:
      print("Error in connection")
      sys.stdout.flush()
   
channel = connection.channel()
channel.exchange_declare(exchange='incoming',
                         exchange_type='fanout')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='incoming',
                   queue=queue_name)

def callback(ch, method, properties, body):
    print(" [x] %r" % body)
    sys.stdout.flush()
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_consume(callback,
                      queue=queue_name)

channel.start_consuming()
