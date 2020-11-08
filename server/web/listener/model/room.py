from sqlalchemy.exc import IntegrityError, OperationalError, ProgrammingError
from flask import current_app as app

from listener.module import generate_uuid
from listener.model.globals import db

class Room(db.Model):
    __tablename__ = "room"
    uuid = db.Column(db.String(64), primary_key=True)
    apikey = db.Column(db.String(app.config['KEY_LENGTH']), unique=True)
    name = db.Column(db.String(100), unique=True)

    def __init__(self, name, apikey):
        self.uuid = str(generate_uuid())
        self.apikey = str(apikey)
        self.name = str(name)
