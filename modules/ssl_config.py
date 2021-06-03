from modules.config import Config
from ssl import SSLContext, PROTOCOL_TLS_SERVER
from pathlib import Path


class SSlConfig:
    """
        Helper to get SSL Context with SSL contract describe in configuration file
    """

    @staticmethod
    def get_context(root_dir: str) -> SSLContext:
        ssl_cert_path = Config.get('Server', 'SslCrt')
        ssl_key_path = Config.get('Server', 'SslKey')

        ssl_cert_file = Path(root_dir, ssl_cert_path)
        ssl_key_file = Path(root_dir, ssl_key_path)
        ssl_context = SSLContext(PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(ssl_cert_file, ssl_key_file)

        return ssl_context
