from flask import Flask
from sqlalchemy.engine.url import make_url
from sqlalchemy.exc import InternalError, OperationalError, ProgrammingError
from sqlalchemy_utils import database_exists, create_database

def init_app(config="listener.config.Production"):
    app = Flask(__name__, template_folder="view")
    
    with app.app_context():
        app.config.from_object(config)

        from listener.model.globals import db
        db_url = make_url(app.config["SQLALCHEMY_DATABASE_URI"])

        if not db_url.drivername.startswith("sqlite"):
            app.config["SQLALCHEMY_POOL_SIZE"] = 100
            app.config["SQLALCHEMY_POOL_RECYCLE"] = 300

            if db_url.drivername.startswith("mysql"):
                db_url.query["charset"] = "utf8mb4"
            elif db_url.drivername == "postgres":
                db_url.drivername == "postgresql"

        if not database_exists(db_url):
            try:
                if db_url.drivername.startswith("mysql"):
                    create_database(db_url, encoding="utf8mb4")
                else:
                    create_database(db_url)
            except Exception as e:
                return False

        app.config["SQLALCHEMY_DATABASE_URI"] = str(db_url)
        db.init_app(app)

        try:
            from listener.model.room import Room
            from listener.model.booking import Booking
            db.create_all()
        except InternalError as e:
            return None
        except (ProgrammingError, OperationalError) as e:
            db.session.rollback()
            return False
        finally:
            app.db = db
            db.session.close()


        from listener.controller.sensor import sensors
        app.register_blueprint(sensors)
        from listener.controller.admin import admin
        app.register_blueprint(admin)
        from listener.controller.ui import ui
        app.register_blueprint(ui)
    return app
