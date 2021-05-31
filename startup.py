import asyncio
import sys
import os
import websockets
from modules.socket_server import WebSocketServer
from modules.logger import AppLogger

logger = AppLogger().get_logger("Main")

async def main():
    logger.info("Application started")

    ws_server = WebSocketServer()
    start_server = await websockets.serve(lambda websocket, path: ws_server.connection_handler(websocket, path), "localhost", 8765)

    logger.info("Web socket server started")
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
