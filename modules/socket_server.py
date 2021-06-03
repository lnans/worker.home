from asyncio import wait
from ssl import SSLContext
from modules.logger import AppLogger
from modules.system_worker import SystemInfoWorker
from websockets.legacy.server import WebSocketServerProtocol, Serve
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK


class WebSocketServerSecure:
    """
        Web socket server
        Handle multiple client connection
        Use to send system hardware information on connected clients
    """

    __host: str
    __port: int
    __ssl_context: SSLContext
    __logger: AppLogger
    __system_worker: SystemInfoWorker
    __clients: set

    def __init__(self, host: str, port: int, ssl_context: SSLContext) -> None:
        self.__logger = AppLogger(type(self).__name__)
        self.__clients = set()
        self.__host = host
        self.__port = port
        self.__ssl_context = ssl_context
        self.__system_worker = SystemInfoWorker()
        self.__system_worker.onChangeAsync += self.send_to_clients

    """ Starting server and infinite wait """
    async def start(self) -> None:
        server = await Serve(self.connection_handler, self.__host, self.__port, ssl=self.__ssl_context)
        self.__logger.info(f'Web socket server started on [wss://{self.__host}:{self.__port}]')
        await server.wait_closed()

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
        except ConnectionClosedOK:
            pass
        except ConnectionClosedError:
            pass
        finally:
            await self.unregister_client(ws)
