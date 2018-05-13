import os.path
path = os.path.dirname(__file__)
if path == '': path = '.'

from src.server import GameServer
GameServer(path).start()
