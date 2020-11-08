from flask import Flask

def init_app(config="listener.config.Production"):
    app = Flask(__name__, template_folder="view")
    
    with app.app_context():
        app.config.from_object(config)

        from listener.controller.sensor import sensors
        app.register_blueprint(sensors)
        from listener.controller.admin import admin
        app.register_blueprint(admin)
    return app
