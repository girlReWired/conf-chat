import zmq
import socket
import threading


class Peer:
    def __init__(self):
        # Automatically get local IP address and port
        self.ip = self.get_local_ip()
        self.port = self.get_available_port()

        self.context = zmq.Context()
        self.peers = set()
        self.messages = []

        # Socket for receiving messages
        self.receiver_socket = self.context.socket(zmq.REP)
        self.receiver_socket.bind(f"tcp://{self.ip}:{self.port}")

        # Thread for listening to messages
        threading.Thread(target=self.listen_for_messages, daemon=True).start()

        print("Welcome to the P2P Chat System!")
        print(f"Your assigned IP and Port: {self.ip}:{self.port}")
        print("Share this with others to connect with you.")

    def get_local_ip(self):
        """Get the local IP address of the machine."""
        try:
            # Create a dummy socket to determine the IP address
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        except Exception:
            return "127.0.0.1"  # Fallback to localhost

    def get_available_port(self):
        """Find an available port dynamically."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))  # OS assigns an available port
            return s.getsockname()[1]

    def listen_for_messages(self):
        """Continuously listen for messages from peers."""
        while True:
            try:
                message = self.receiver_socket.recv_json()
                msg_type = message.get("type")
                if msg_type == "message":
                    # Display received message
                    sender_ip = message["sender_ip"]
                    sender_port = message["sender_port"]
                    text = message["message"]
                    print(f"\n--- New Message ---\nFrom {sender_ip}:{sender_port}\n{text}\n-------------------")
                elif msg_type == "register":
                    # Handle peer registration
                    peer_ip = message["ip"]
                    peer_port = message["port"]
                    self.peers.add((peer_ip, peer_port))
                    self.receiver_socket.send_json({"status": "success", "message": "Registered successfully"})
                    print("\n\n--- New Peer Registered ---")
                    print(f"{peer_ip}:{peer_port}")
                    print("----------------------------\n")
                    self.show_prompt()  # Display prompt after handling registration
                else:
                    self.receiver_socket.send_json({"status": "error", "message": "Unknown request"})
            except Exception as e:
                print(f"Error receiving message: {e}")

    def register_with_peer(self, peer_ip, peer_port):
        """Register this peer with another peer."""
        try:
            socket = self.context.socket(zmq.REQ)
            socket.connect(f"tcp://{peer_ip}:{peer_port}")
            socket.send_json({
                "type": "register",
                "ip": self.ip,
                "port": self.port
            })
            response = socket.recv_json()
            if response.get("status") == "success":
                self.peers.add((peer_ip, peer_port))
                print("\n--- New Peer Registered ---")
                print(f"{peer_ip}:{peer_port}")
                print("----------------------------\n")
            else:
                print(f"Error registering with peer: {response.get('message')}")
        except Exception as e:
            print(f"Error connecting to peer: {e}")

    def send_message(self, peer_ip, peer_port, message):
        """Send a message to a specific peer."""
        try:
            socket = self.context.socket(zmq.REQ)
            socket.connect(f"tcp://{peer_ip}:{peer_port}")
            socket.send_json({
                "type": "message",
                "message": message,
                "sender_ip": self.ip,
                "sender_port": self.port
            })
            response = socket.recv_json()
            if response.get("status") == "success":
                print(f"Message sent to {peer_ip}:{peer_port}")
            else:
                print(f"Error sending message: {response.get('message')}")
        except Exception as e:
            print(f"Error sending message: {e}")

    def display_peers(self):
        """Display all connected peers."""
        if not self.peers:
            print("No peers connected.")
        else:
            print("\n--- Connected Peers ---")
            for peer_ip, peer_port in self.peers:
                print(f"{peer_ip}:{peer_port}")
            print("-----------------------")

    def show_prompt(self):
        """Show the option prompt at the bottom."""
        print("\nOptions:")
        print("1. Register with a peer")
        print("2. Send a message")
        print("3. Display connected peers")
        print("4. Exit")
        print("Choose an option: ", end="", flush=True)


if __name__ == "__main__":
    peer = Peer()

    while True:
        peer.show_prompt()
        choice = input()

        if choice == "1":
            peer_ip = input("Enter IP of a peer to register with: ")
            peer_port = input("Enter port of the peer: ")
            peer.register_with_peer(peer_ip, int(peer_port))

        elif choice == "2":
            peer_ip = input("Enter IP of the peer to message: ")
            peer_port = input("Enter port of the peer: ")
            message = input("Enter your message: ")
            peer.send_message(peer_ip, int(peer_port), message)

        elif choice == "3":
            peer.display_peers()

        elif choice == "4":
            print("Exiting...")
            break

        else:
            print("Invalid option. Please try again.")


