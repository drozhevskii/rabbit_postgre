from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
import pika
import logging
import psycopg2
import psycopg2
from config import load_config

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'sent'

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

def create_tables():

    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # execute the CREATE TABLE statement
                cur.execute('''
        CREATE TABLE IF NOT EXISTS images (
            image_id SERIAL PRIMARY KEY,
            image_name VARCHAR(255) NOT NULL,
            image_status VARCHAR(255) NOT NULL,
            date_processed TIMESTAMP
        )
        ''')
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def insert_send(filename):

    sql = """INSERT INTO images(image_name, image_status, date_processed)
             VALUES(%s,'sent', current_timestamp) RETURNING image_id;"""
    
    image_id = None
    config = load_config()

    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                # execute the INSERT statement
                cur.execute(sql, (filename,))

                # get the generated id back                
                rows = cur.fetchone()
                if rows:
                    image_id = rows[0]

                # commit the changes to the database
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)    
    finally:
        return image_id
    
def insert_receive(filename):

    sql = """INSERT INTO images(image_name, image_status, date_processed)
             VALUES(%s,'received', current_timestamp) RETURNING image_id;"""
    
    image_id = None
    config = load_config()

    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                # execute the INSERT statement
                cur.execute(sql, (filename,))

                # get the generated id back                
                rows = cur.fetchone()
                if rows:
                    image_id = rows[0]

                # commit the changes to the database
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)    
    finally:
        return image_id

def send(filename):
    path = 'sent/{val}'.format(val = filename)
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
    connection.close()
    #channel.start_consuming()


@app.route('/', methods=['GET',"POST"])
@app.route('/home', methods=['GET',"POST"])

def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data # grab the file
        filename = file.filename
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # save the file
        send(filename) #send the file to q
        create_tables()
        insert_send(filename)
        
        receive(file.filename) #receive the file
        insert_receive(file.filename)

        return "File has been uploaded."

    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')