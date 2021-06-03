import asyncio
import sys
import os
import websockets
import ssl
from pathlib import Path
from modules.config import Config
from modules.socket_server import WebSocketServer
from modules.logger import AppLogger

MAIN_DIR = Path(__file__).resolve().parent
LOGGER = AppLogger().get_logger('Main')

async def main():
    LOGGER.info('Application started')

    # Reading conf
    LOGGER.info('Reading CONF')
    host = Config.get('Server', 'Host')
    port = Config.get_int('Server', 'Port')
    ssl_cert = Config.get('Server', 'SslCrt')
    ssl_key = Config.get('Server', 'SslKey')

    # Load SSL context
    LOGGER.info('Load SSL configuration')
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(Path(MAIN_DIR, ssl_cert), Path(MAIN_DIR, ssl_key))

    # Starting web socket server
    LOGGER.info('Starting web socket server...')
    ws_server = WebSocketServer()
    start_server = await websockets.serve(lambda websocket, path: ws_server.connection_handler(websocket, path), host, port, ssl=ssl_context)

    LOGGER.info(f'Web socket server started on [wss://{host}:{port}]')

    # Infinite wait
    await start_server.wait_closed()

# Main section
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except BaseException as e:
        LOGGER.error(e, exc_info=True)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
