import pika
import logging

def send(filename):
    path = 'imgs/{val}'.format(val = filename)
    print(path)
    f=open(path, 'rb')
    i=f.read()
    #os.remove(full_path)
    logging.basicConfig()
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='imageq')

    channel.basic_publish(exchange='',routing_key='imageq',body=i)
    print("[x] Sent image")
    connection.close()

#filename="dis_pic_awaken.jpg"
#(filename)