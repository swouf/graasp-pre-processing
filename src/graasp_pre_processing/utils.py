from datetime import datetime
from pandera import Parser


def timestamp_convert(t):
    if isinstance(t, str):
        return datetime.fromisoformat(t)
    else:
        return t

timestamp_parser = Parser(timestamp_convert)