from uuid import uuid4
from datetime import datetime

def generate_uuid(hex=True):
    """
    Generates a RFC-4122 compliant UUID.

    Arguments:
        hex         (Boolean):      Output in hex.

    Returns:
        [Success]
            String:                 UUID.
    """
    if hex:
        return str(uuid4().hex)
    return str(uuid4())

def convert_timestamp_to_time(timestamp, pattern="%d/%m/%Y %H:%M"):
    return datetime.fromtimestamp(timestamp).strftime(pattern)

def convert_time_to_timestamp(time, pattern="%d/%m/%Y %H:%M"):
    return datetime.strptime(time, pattern).timestamp()
