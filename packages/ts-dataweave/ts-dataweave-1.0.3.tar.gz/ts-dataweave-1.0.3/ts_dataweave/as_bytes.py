from json import dumps

def as_bytes(data) -> bytes:
    """Converts the input into bytes. Input data should be a Payload, string, bytes,
    dict, list, or a file-like object.

    Args:
        data: input data

    Returns:
        bytes: bytes representation of the input data
    """

    bytes_data = None

    if isinstance(data, str):
        bytes_data = data.encode("utf-8")

    elif isinstance(data, bytes):
        bytes_data = data

    elif isinstance(data, dict) or isinstance(data, list):
        bytes_data = dumps(data).encode("utf-8")

    else:
        read_f = getattr(data, "read", None)
        if callable(read_f):
            bytes_data = read_f()

    return bytes_data
