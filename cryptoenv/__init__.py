from .web import runserver

from .core import Configuration
from .crypto import DecryptedConfig, KeyGenerator, Crypto


def run_web_app():
    print("Hello world")
    runserver()
