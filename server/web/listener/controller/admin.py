from flask import current_app as app, Blueprint, request, render_template
from listener.model.room import Room, get_room
from listener.model.booking import Booking, get_booking
from listener.module import convert_time_to_timestamp, convert_timestamp_to_time

admin = Blueprint("admin", __name__)

@admin.route('/room', methods=['GET'])
def h_get_room():
    '''
    Handles GET request for /room endpoint
    '''
    rooms = {}
    for room in get_room() or []:
        rooms[room.uuid] = room.name
    return rooms


@admin.route('/room', methods=['POST'])
def h_post_room():
    '''
    Handles POST request for /room endpoint

    Form Values:
        name -- Name of the room
    '''
    name = request.form.get('name')
    if not name:
        return 'Missing argumments', 400
    room = Room(name)
    apikey = room.apikey
    result = room.add()
    if result:
        return apikey, 200
    elif isinstance(result, bool):
        return 'Room name cannot be duplicated', 400
    elif result is None:
        return 'An Unexpected Error Occurred', 500

@admin.route('/booking', methods=['GET'], defaults={"room":None})
@admin.route('/booking/<room>', methods=['GET'])
def h_get_booking(room):
    '''
    Handles GET request for /booking endpoint
    Booking for a specific room can be retrieved at /booking/room_uuid
    '''
    if room:
        bookings = get_booking(room=room) or []
    else:
        bookings = get_booking() or []
    
    result = {}
    for b in bookings:
        start = convert_timestamp_to_time(b.start_time)
        end =  convert_timestamp_to_time(b.end_time)
        result[b.uuid] = {'room': b.room_uuid, 'start': start, 'end': end}
    return result


@admin.route('/booking', methods=['POST'])
def h_post_booking():
    '''
    Handles POST request for /booking endpoint
    This endpoint assumes all time submitted is in the timezone of Asia/Singapore
    
    Form Values:
        room -- Room UUID. Value should be retrieved from GET /room endpoint
        date -- Date of booking (Format -- DD/MM/YYYY)
        start -- Start Time     (Format -- HH:MM)
        end -- End Time         (Format -- HH:MM)
    '''
    room = request.form.get('room')
    date = request.form.get('date')
    start = request.form.get('start')
    end = request.form.get('end')
    if not room or not date or not start or not end:
        return 'Missing arguments', 400
    
    start = '{} {}'.format(date, start)
    end = '{} {}'.format(date, end)
    t_format = "%d/%m/%Y %H:%M"
    start = convert_time_to_timestamp(start)
    end = convert_time_to_timestamp(end)

    if end <= start:
        return 'End time should be later than start time', 400

    booking = Booking(room, start, end)
    result = booking.add()
    if result:
        return '', 204
    elif isinstance(result, bool):
        return 'Room is not available for booking', 400
    elif result is None:
        return 'An Unexpected Error Occurred', 500
