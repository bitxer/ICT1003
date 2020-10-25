from flask import Flask

def init_app(config="app.config.Production"):
    app = Flask(__name__)
    with app.app_context():
        app.config.from_object(config)

    return app