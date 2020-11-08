from uuid import uuid4

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
