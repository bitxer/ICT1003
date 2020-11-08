from flask import Flask

def init_app(config="listener.config.Production"):
    app = Flask(__name__)
    with app.app_context():
        app.config.from_object(config)

        from listener.endpoint import endpoints
        app.register_blueprint(endpoints)
    return app
