#!/usr/bin/python3
class NotImplemented(Exception):
    pass


class GenericInterface:
    def __init__(self, backend_url: str, bucket: str):
        pass

    def send(
        self,
        timestamp_ns: int,
        name: str,
        value: float,
        tags: map = {},
    ):
        raise NotImplemented
