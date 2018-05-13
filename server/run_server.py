import os.path

import env

path = os.path.dirname(__file__)
if path == '': path = '.'

from src.server import GameServer
GameServer(env).start()
