from flask import current_app as app, Blueprint, request, render_template
from secrets import token_urlsafe
from listener.model.room import Room

admin = Blueprint("admin", __name__)

@admin.route('/room', methods=['GET', 'POST'])
def door():
    if request.method == 'GET':
        return render_template('room.html')
    else:
        name = request.form.get('name')
        apikey = token_urlsafe(app.config['KEY_LENGTH'])
        room = Room(name, apikey)
        room.add()
        return render_template('result.html', message="Room added successfully", key=apikey)

@admin.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'GET':
        rooms = {'id1': 'Room 1', 'id2': 'Room 2'}
        return render_template('booking.html', rooms=rooms)
    else:
        return render_template("result.html", message="Room booking successful")