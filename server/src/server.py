from serverlogic import storage, serverfuncts, gamefuncts

import re
from TwistedWebsocket.server import Protocol
from twisted.internet.protocol import ServerFactory
from json import JSONDecoder, JSONEncoder

class GameProtocol(Protocol):
    """Websocket protocol for game clients."""
    def onHandshake(self, header):
        """Overloaded handshake function."""
        g = re.search('Origin\s*:\s*(\S+)', header)
        if not g: return
        print 'handshake successful'

    def onConnect(self):
        """Overloaded connect function."""
        print 'connection made'
        if self.factory.isFull():
            # Send server full error message
            serverfuncts.sendResp(self, {'err':'The server is full'})
            # Close connection
            self.abortConnection()
        else:
            # Add client to server
            self.factory.clients.append(self)
            # Init client attributes
            self.status = 'Logging in'
            self.name = None
            self.gamekey = None
            self.playerdata = None

            serverfuncts.sendResp(self, {})

    def onMessage(self, raw_data):
        """Overloaded message function."""
        serverfuncts.logMsg('from: '+str(self.name) + " - " + raw_data)
        # Parse message data
        data = raw_data.split()
        if len(data) > 0:
            if data[0] == 'disconnect':
                serverfuncts.closeConn(self)
            elif data[0] == 'create':
                if len(data) > 1 and data[1] == 'user':
                    serverfuncts.createUser(self, data)
                elif len(data) > 1 and data[1] == 'game':
                    serverfuncts.createGame(self, data)
            elif data[0] == 'login':
                serverfuncts.login(self, data)
            elif data[0] == 'logout':
                serverfuncts.logout(self)
            elif data[0] == 'join':
                if len(data) > 1 and data[1] == 'game':
                    serverfuncts.joinGame(self, data)
            elif data[0] == 'levelup':
                serverfuncts.levelup(self, data)
            elif data[0] == 'quit':
                if len(data) > 1 and data[1] == 'game':
                    serverfuncts.quitGame(self)
            elif data[0] == 'attack':
                gamefuncts.attack(self, data)
            elif data[0] == 'defend':
                gamefuncts.defend(self, data)
            else:
                pass
"""
        except IndexError as e:
            # Send error message with status-specific data
            resp = {}
            resp['err'] = 'malformed command'
            serverfuncts.addStatusInfo(self, resp)
            self.sendMessage(self.factory.json_encoder.encode(resp))
            # Log
            serverfuncts.logMsg('to: '+str(self.name)+" - "+str(resp))
            print e

        except KeyError as e:
            # Send error message with status-specific data
            resp = {}
            resp['err'] = 'malformed command'
            serverfuncts.addStatusInfo(self, resp)
            self.sendMessage(self.factory.json_encoder.encode(resp))
            # Log
            serverfuncts.logMsg('to: '+str(self.name)+" - "+str(resp))
            print e
"""
class GameServerFactory(ServerFactory):
    """Websocket factory for game server."""
    def __init__(self, proto, env):
        """Overloaded constructor."""
        # Link protocol
        self.protocol = proto
        self.env = env
        # Init server data
        self.clients = []
        self.named_clients = {}
        self.games = {}
        # Init decoders
        self.json_decoder = JSONDecoder()
        self.json_encoder = JSONEncoder()
        # Init configs
        serverfuncts.configLog(self.env.log_path + '/server.log')

    def isFull(self):
        """Determines if the number of clients has reached its limit.
        Client limit is a server property."""
        return len(self.clients) >= int(self.env.client_limit)

    def sendToAll(self, msg):
        """Send to all connected clients."""
        for c in self.clients:
            c.sendMessage(msg)

    def sendToClients(self, clientnames, msg):
        """Send to all specified logged in clients."""
        for name in clientnames:
            if name in self.named_clients.keys():
                self.named_clients[name].sendMessage(msg)

from twisted.internet import reactor

class GameServer(object):
    """Server class"""
    def __init__(self, env):
        """Constructor"""
        self.env = env
        # Set onstop trigger
        reactor.addSystemEventTrigger('before', 'shutdown', self.onStop)
        # Set up server
        svrfactory = GameServerFactory(GameProtocol, env)
        reactor.listenTCP(int(self.env.server_port), svrfactory)

    def start(self):
        """Start the server."""
        reactor.run()

    def onStop(self):
        """Clean up before the server stops."""
        pass
