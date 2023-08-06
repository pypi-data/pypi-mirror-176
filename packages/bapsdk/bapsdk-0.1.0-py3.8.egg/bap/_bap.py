import json
import socket


class Bap(object):
    _ADDR = ('host.docker.internal', 8081)

    def __init__(self, api_key: str):
        self._api_key = api_key
        self._socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    async def handle_update(self, update: dict):
        data = json.dumps({
            'api_key': self._api_key,
            'update': update
        })
        self._socket.sendto(data, self._ADDR)
