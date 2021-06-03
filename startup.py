import asyncio
import sys
import os
import websockets
from configparser import ConfigParser
from modules.socket_server import WebSocketServer
from modules.logger import AppLogger

logger = AppLogger().get_logger('Main')
config = ConfigParser()

async def main():
    # Reading conf
    config.read('.config.ini')
    host = config.get('Settings', 'Host')
    port = config.getint('Settings', 'Port')

    logger.info('Application started')

    # Starting web socket server
    ws_server = WebSocketServer()
    start_server = await websockets.serve(lambda websocket, path: ws_server.connection_handler(websocket, path), host, port)

    logger.info(f'Web socket server started on [ws://{host}:{port}]')

    # Infinite wait
    await start_server.wait_closed()

# Main section
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except BaseException as e:
        logger.error(e, exc_info=True)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
