from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
import pika
import logging

#import send_function
#import receive_function

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'imgs'

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

def send(filename):
    path = 'imgs/{val}'.format(val = filename)
    print(path)
    f=open(path, 'rb')
    i=f.read()

    logging.basicConfig()
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='imageq')

    channel.basic_publish(exchange='',routing_key='imageq',body=i)
    print("[x] Sent image")
    connection.close()

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


@app.route('/', methods=['GET',"POST"])
@app.route('/home', methods=['GET',"POST"])

def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data # grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # save the file
        send(file.filename) #send the file to q
        #print('received/{val}'.format(val = file.filename))
        receive(file.filename) #receive the file
        return "File has been uploaded."
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)