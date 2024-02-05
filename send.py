import pika
import logging
import os

path = 'imgs/'
full_path = os.path.join(path, os.listdir(path)[0])
f=open(full_path,'rb')
i=f.read()

logging.basicConfig()
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='imageq')

channel.basic_publish(exchange='',routing_key='imageq',body=i)
print("[x] Sent image")
connection.close()