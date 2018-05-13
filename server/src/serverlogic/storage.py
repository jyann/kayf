from os import path

def getPlayers(env, decoder):
    """Get all players in storage"""
    file_path = env.storage_path + '/players.json'
    if path.exists(file_path):
        players = decoder.decode(open(file_path, 'r').read())
    else:
        players = {}
    return players

def getPlayer(env, name, decoder):
    """Get user's player data"""
    players = getPlayers(env, decoder)

    if name in players.keys():
        return players[name]
    else:
        return False

def storePlayerData(env, name, data, encoder, decoder):
    """Store user's player data"""
    file_path = env.storage_path + '/players.json'
    players = getPlayers(env, decoder)
    players[name] = data
    open(file_path, 'w').write(encoder.encode(players))
