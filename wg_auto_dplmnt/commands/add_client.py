import os, subprocess

WG_DIR = "/etc/wireguard/"
WG_SERVER_CONFIG_PATH = "/etc/wireguard/wg0.conf"

class NameParser():
    @staticmethod
    def parse_filename():
        files = os.listdir(WG_DIR)

        client_keys = [f for f in files if f.startswith("client") and f.endswith("_private.key")]

        client_indicies = []

        for key in client_keys:
            client_index = key.replace("client", "").replace("_private.key", "")
            client_indicies.append(int(client_index))

        if client_indicies:
            new_client_index = max(client_indicies) + 1
        else:
            new_client_index = 1

        return new_client_index
    
    @staticmethod
    def parse_ip():
        clients_ips = []
        with open(WG_SERVER_CONFIG_PATH) as f:
            for line in f:
                if line.startswith("AllowedIPs"):
                    ip = line.split("=")[1].strip()

                    clients_ips.append(int(ip.split(".")[3]))
        
        if clients_ips:
            new_client_ip_index = max(clients_ips) + 1
        else:
            new_client_ip_index = 2

        new_client_ip = f"10.8.0.{new_client_ip_index}/32"

        return new_client_ip
    
class AddClientCommand():
    def generate_private_key(self):
        print("Generating new private key...")

        client_index = NameParser.parse_filename()
        new_client_path = f"{WG_DIR}client{client_index}_private.key"

        cmd = f"wg genkey | tee {new_client_path}"

        subprocess.run(cmd, shell=True, check=True)

        print("Private key generated")

        self.generate_public_key(new_client_path, client_index)

    def generate_public_key(self, path, index):
        print("Generating new public key...")

        cmd = f"cat {path} | wg pubkey | tee {WG_DIR}client{index}_public.key"

        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)

        public_key = result.stdout.strip()

        print("Public key generated")

        self.add_peer_to_server_config(public_key)

    def add_peer_to_server_config(self, public_key):
        print("Adding new client to server config")

        client_ip = NameParser.parse_ip()

        peer_block = f"\n[Peer]\nPublicKey = {public_key}\nAllowedIPs = {client_ip}\n"

        with open(WG_SERVER_CONFIG_PATH, "a") as f:
            f.write(peer_block)

        print("DONE! New client successfully added")