import os

DETECTION_URL = "https://ict1003.yongze.dev/detection"
ROOM_KEY = os.getenv('ROOM_KEY')
CAMERA_FOLDER = os.getenv('CAMERA_FOLDER') or './camera'
ALLOWED_MAC = ["c5:2d:cc:32:65:34"]
