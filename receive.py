import pika
import sys

def receive(filename):
    f=open('received/{val}'.format(val = filename),'wb')
    #f=open('received/imagetest.jpg','wb')
    connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='imageq')

    print(" [*] Waiting for images")

    def callback(ch, method, properties, body):
        f.write(body)
        f.close()
        print(" [*] Image received")

    channel.basic_consume('imageq', callback, auto_ack=True)
    channel.start_consuming()

#receive(filename)