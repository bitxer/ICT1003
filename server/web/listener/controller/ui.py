from flask import current_app as app, Blueprint, request, render_template
from listener.model.room import Room, get_room
from listener.model.booking import Booking, get_booking
from listener.module import convert_time_to_timestamp, convert_timestamp_to_time

ui = Blueprint("ui", __name__)


@ui.route('/ui/rooms', methods=['GET'])
def rooms():
    rooms = {}
    for room in get_room() or []:
        rooms[room.uuid] = room.name
    print(rooms)
    return render_template('room.html', rooms=rooms)
