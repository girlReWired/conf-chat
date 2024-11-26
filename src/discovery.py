class PeerDiscovery:
    def __init__(self):
        self.peers = {}

    def add_peer(self, username, address, port):
        self.peers[username] = {"address": address, "port": port}

    def get_peer(self, username):
        return self.peers.get(username)

    def list_peers(self):
        return self.peers
