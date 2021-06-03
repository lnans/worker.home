import asyncio
import sys
import os
from pathlib import Path
from modules.config import Config
from modules.socket_server import WebSocketServerSecure
from modules.logger import AppLogger
from modules.ssl_config import SSlConfig

ROOT_DIR = Path(__file__).resolve().parent
LOGGER = AppLogger('Main')

class Startup:

    @staticmethod
    async def main():
        LOGGER.info('Application started')

        # Starting web socket server
        host = Config.get('Server', 'Host')
        port = Config.get_int('Server', 'Port')
        ssl_context = SSlConfig.get_context(ROOT_DIR)
        ws_server = WebSocketServerSecure(host, port, ssl_context)
        await ws_server.start()


# Main section
if __name__ == '__main__':
    try:
        asyncio.run(Startup.main())
    except BaseException as e:
        LOGGER.error(e, exc_info=True)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
