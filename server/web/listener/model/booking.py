from sqlalchemy.exc import IntegrityError, OperationalError, ProgrammingError

from listener.module import generate_uuid
from listener.model.globals import db

class Booking(db.Model):
    __tablename__ = "booking"
    uuid = db.Column(db.String(32), primary_key=True)
    room_uuid = db.Column(db.String(32), db.ForeignKey("room.uuid"), nullable=False)
    start_time = db.Column(db.Integer)
    end_time = db.Column(db.Integer)

    def __init__(self, room_uuid, start, end):
        self.uuid = str(generate_uuid())
        self.room_uuid = room_uuid
        self.start_time = int(start)
        self.end_time = int(end)

    def add(self):
        try:
            bookings = get_booking(room=self.room_uuid)
            if bookings:
                for book in bookings:
                    b_starttime = book.start_time
                    b_endtime = book.end_time
                    if (b_starttime <= self.start_time and self.start_time < b_endtime) or \
                        (b_starttime < self.end_time and self.end_time <= b_endtime) or \
                            (self.start_time < b_starttime and b_endtime < self.end_time):
                        return False
            db.session.add(self)
            db.session.commit()
            return True
        except (IntegrityError, ProgrammingError, OperationalError) as e:
            print(e)
            db.session.rollback()
            return None
        finally:
            db.session.close()

def get_booking(uuid=None, room=None):
    try:
        if uuid:
            return Booking.query.filter_by(uuid=uuid).first() or False
        elif room:
            return Booking.query.filter_by(room_uuid=room).all() or False
        return Booking.query.all() or False
    except (ProgrammingError, OperationalError):
        return None
    finally:
        db.session.close()
