from flask import current_app as app, Blueprint, request, render_template
from listener.model.room import Room, get_room

admin = Blueprint("admin", __name__)

@admin.route('/room', methods=['GET', 'POST'])
def door():
    if request.method == 'GET':
        return render_template('room.html')
    else:
        name = request.form.get('name')
        room = Room(name)
        apikey = room.apikey
        result = room.add()
        if result:
            message = "Room added successfully"
            return render_template('result.html', message=message, key=apikey)
        elif isinstance(result, bool):
            message = "Room name cannot be duplicated"
            return render_template('result.html', message=message)
        elif result is None:
            message = "An error occurred"
            return render_template('result.html', message=message)

@admin.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'GET':
        rooms = get_room()
        return render_template('booking.html', rooms=rooms)
    else:
        return render_template("result.html", message="Room booking successful")