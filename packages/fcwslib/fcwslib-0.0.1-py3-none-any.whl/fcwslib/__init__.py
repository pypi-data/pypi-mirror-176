__author__ = 'Fackcraft'
__version__ = '0.0.1'
__all__ = ['Handler', 'Server', 'build_header']

import asyncio
import json
from uuid import uuid4

import websockets


class Handler:
    def __init__(self, websocket) -> None:
        self._websocket = websocket
        self._command_responses: dict = dict()
        self._subscribed_events: dict = (dict(), dict())

    async def _on_connect(self) -> None:
        task = asyncio.get_event_loop().create_task(self.on_connect())

        while True:
            try:
                message: str = json.loads(await self._websocket.recv())
            except websockets.exceptions.ConnectionClosedOK:
                await self.on_disconnect()
                break
            else:
                response_id: str = message['header']['requestId']

                if message['header']['messagePurpose'] == 'commandResponse':
                    func = self._command_responses[response_id]
                    del self._command_responses[response_id]
                else:
                    func = self._subscribed_events[response_id]
                
                if func:
                    await func(message)

        await task

    async def on_connect(self) -> None:
        pass

    async def on_disconnect(self) -> None:
        pass

    async def on_receive(self, message: str) -> None:
        pass

    async def send(self, message: str) -> None:
        await self._websocket.send(message)

    async def send_command(self, command: str, callback=None) -> None:
        request_id: str = str(uid.uuid4())

        self._command_responses[request_id] = callback

        message = {
            'header': build_header('commandRequest', request_id=request_id),
            'body': {
                'origin': {
                    'type': 'player'
                },
                'commandLine': command,
                'version': 1
            }
        }

        await self.send(json.dumps(message))

    async def subscribe(self, event_name: str, callback=None) -> None:
        request_id: str = str(uuid.uuid4())

        self._subscribed_events[0][request_id] = callback
        self._subscribed_events[1][event_name] = request_id

        await self.send(json.dumps({
            'header': build_header('subscribe', request_id=request_id),
            'body': {
                'eventName': str(event_name)
            }
        }))
    
    async def unsubscribe(self, event_name: str) -> None:
        del self._subscribed_events[0][self._subscribed_events[1][event_name]]
        del self._subscribed_events[1][event_name]

        await self.send(json.dumps({
            'header': build_header('unsubscribe'),
            'body': {
                'eventName': str(event_name)
            }
        }))


class Server(object):
    def __init__(self, host: str = '127.0.0.1', port: int = 8000) -> None:
        self._host: str = host
        self._port: int = port
        self._handlers: list = list()
        self._connections: list = list()

    def insert_handler(self, handler) -> None:
        self._handlers.append(handler)

    def remove_handler(self, handler) -> None:
        self._handlers.remove(handler)

    def handlers(self) -> list:
        return self._handlers

    async def run_forever(self):
        async with websockets.serve(self._on_connect, self._host, self._port):
            await asyncio.Future()

    async def _on_connect(self, websocket, _) -> None:
        connection: list = list()
        tasks: list = list()

        for Handler in self._handlers:
            handler = Handler(websocket)
            connection.append(Handler)
            tasks.append(asyncio.create_task(handler._on_connect()))

        self._connections.append(connection)

        for task in tasks:
            await task


def build_header(purpose: str, request_id: str = None) -> dict:
    if request_id is None:
        request_id: str = str(uuid.uuid4())

    return {
        'requestId': request_id,
        'messagePurpose': purpose,
        'version': 1,
        'messageType': 'commandRequest'
    }

