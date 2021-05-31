from asyncio import wait
from logging import Logger
from modules.logger import AppLogger
from modules.system_worker import SystemInfoWorker
from websockets.legacy.server import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedError


class WebSocketServer:
    """
        Web socket server
        Handle multiple client connection
        Use to send system hardware information on connected clients
    """

    __logger: Logger
    __system_worker: SystemInfoWorker
    __clients: set

    def __init__(self) -> None:
        self.__logger = AppLogger().get_logger(type(self).__name__)
        self.__clients = set()
        self.__system_worker = SystemInfoWorker()
        self.__system_worker.onChangeAsync += self.send_to_clients

    """ Register a new client """
    async def register_client(self, ws: WebSocketServerProtocol) -> None:
        self.__clients.add(ws)
        self.__logger.info(f'{ws.remote_address} connects.')

    """ Unregister a client """
    async def unregister_client(self, ws: WebSocketServerProtocol) -> None:
        self.__clients.remove(ws)
        self.__logger.info(f'{ws.remote_address} disconnects.')

    """ Send message to all connected clients """
    async def send_to_clients(self, message: str) -> None:
        if len(self.__clients) > 0:
            await wait([client.send(message) for client in self.__clients])

    """ Server connection handler """
    async def connection_handler(self, ws: WebSocketServerProtocol, uri: str) -> None:
        await self.register_client(ws)
        try:
            await ws.recv()
        except ConnectionClosedError:
            pass
        finally:
            await self.unregister_client(ws)
