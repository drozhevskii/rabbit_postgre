import pika

f=open('received/outputimage.jpg','wb')

connection = pika.BlockingConnection(pika.ConnectionParameters(
host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='imageq')

print(" [*] Waiting for messages. To exit press CTRL+C")

def callback(ch, method, properties, body):
    f.write(body)
    f.close()
    channel.basic_consume(callback,
    queue='imageq',
    no_ack=True)

channel.start_consuming()