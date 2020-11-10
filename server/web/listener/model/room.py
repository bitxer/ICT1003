from secrets import token_urlsafe
from sqlalchemy.exc import IntegrityError, OperationalError, ProgrammingError
from flask import current_app as app

from listener.module import generate_uuid
from listener.model.globals import db

class Room(db.Model):
    __tablename__ = "room"
    uuid = db.Column(db.Text, primary_key=True)
    apikey = db.Column(db.Text, unique=True)
    name = db.Column(db.Text, unique=True)
    bookings = db.relationship('Booking', backref='room', lazy=True)

    def __init__(self, name):
        self.uuid = str(generate_uuid())
        self.apikey = str(token_urlsafe(app.config['KEY_LENGTH']))
        self.name = str(name)
    
    def add(self):
        try:
            if get_room(name=self.name) or get_room(apikey=self.apikey):
                return False
            db.session.add(self)
            db.session.commit()
            return True
        except (IntegrityError, ProgrammingError, OperationalError):
            db.session.rollback()
            return None
        finally:
            db.session.close()

def get_room(uuid=None, apikey=None, name=None):
    try:
        if uuid:
            return Room.query.filter_by(uuid=uuid).first() or False
        elif apikey:
            return Room.query.filter_by(apikey=apikey).first() or False
        elif name:
            return Room.query.filter_by(name=name).first() or False
        return Room.query.all() or False
    except (ProgrammingError, OperationalError):
        return None
    finally:
        db.session.close()
