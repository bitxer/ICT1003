import os
from pika import ConnectionParameters, PlainCredentials

class Production:
    DEBUG = False
    TESTING = False
    CONFIG_KEY = "PRODUCTION"
    
    KEY_LENGTH = 48
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') if os.environ.get('UPLOAD_FOLDER') != 'default' else  'APPDATA/uploads'

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    RABBIT_HOST = os.environ.get('RABBIT_HOST') or 'rabbit'
    RABBIT_USER = os.environ.get('RABBIT_USER') or 'guest'
    RABBIT_PASS = os.environ.get('RABBIT_PASS') or 'guest'
    RABBIT_URL = ConnectionParameters(host=RABBIT_HOST, credentials=PlainCredentials(RABBIT_USER, RABBIT_PASS))
    RABBIT_QUEUE = 'ALERT_QUEUE'

class Development(Production):
    DEBUG = True
    CONFIG_KEY = "DEVELOPMENT"

    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL") or "sqlite://"

    RABBIT_URL = ConnectionParameters(host='localhost', credentials=PlainCredentials('guest', 'guest'))
