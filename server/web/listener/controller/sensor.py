from os import path
from json import dumps
from hashlib import md5
from magic import from_buffer
from pika import BlockingConnection, BasicProperties
from flask import current_app as app, Blueprint, request

from listener.model.room import get_room
from listener.model.booking import get_booking
from listener.module import convert_timestamp_to_time

sensors = Blueprint("sensors", __name__)

@sensors.route('/detection', methods=['POST'])
def detection():
    apikey = request.headers.get('X-APIKEY')
    dtime = request.form.get('time')
    image = request.files.get('image')

    if image is None or dtime is None or apikey is None:
        return 'Missing field', 400

    room = get_room(apikey=apikey)
    if not room:
        return '', 403

    try:
        dtime = int(dtime)
    except ValueError:
        return 'Invalid value for time', 400

    try:
        for booking in get_booking(room=room.uuid):
            if dtime >= booking.start_time and dtime <= booking.end_time:
                return '', 204
    except TypeError:
        pass

    f_content = image.read()
    f_type = from_buffer(f_content, mime=True)
    if not f_type.startswith('image'):
        return 'Bad image', 400
    
    f_hash = md5(image.read()).hexdigest()
    f_path = path.join(app.config['UPLOAD_FOLDER'], f_hash)
    with open(f_path, 'wb') as f:
        f.write(f_content)

    conn = BlockingConnection(app.config.get('RABBIT_URL'))
    channel = conn.channel()
    channel.queue_declare(queue='alert', durable=True)
    body = {
        "image": f_hash,
        "room": room.name,
        "time": convert_timestamp_to_time(dtime)
    }
    channel.basic_publish(
        exchange='',
        routing_key='alert',
        body=dumps(body),
        properties=BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    conn.close()
    return '', 204
