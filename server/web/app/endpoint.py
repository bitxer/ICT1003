from flask import current_app as app, Blueprint, request
from magic import from_buffer
from hashlib import md5

import pika, os

endpoints = Blueprint("endpoints", __name__)

@endpoints.route('/detection', methods=['POST'])
def detection():
    apikey = request.headers.get('X-APIKEY')
    if apikey is None:
        return '', 403

    sensor = request.form.get('sensor')
    dtime = request.form.get('time')
    image = request.files.get('image')

    if image is None or sensor is None or dtime is None:
        return 'Missing field', 400

    f_type = from_buffer(image.read(), mime=True)
    if not f_type.startswith('image'):
        return 'Bad image', 400
    
    fname = md5(image.read()).hexdigest()
    fname = os.path.join(app.config['UPLOAD_FOLDER'], fname)
    image.save(fname)

    conn = pika.BlockingConnection(app.config.get('RABBIT_URL'))
    channel = conn.channel()
    channel.queue_declare(queue='alert', durable=True)
    channel.basic_publish(
        exchange='',
        routing_key='alert',
        body=fname,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    conn.close()
    return '', 204
