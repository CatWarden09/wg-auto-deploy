import os, subprocess

WG_DIR = "/etc/wireguard/"
WG_SERVER_CONFIG_PATH = "/etc/wireguard/wg0.conf"


class NameParser:
    @staticmethod
    def parse_filename():
        files = os.listdir(WG_DIR)

        client_keys = [
            f for f in files if f.startswith("client") and f.endswith("_private.key")
        ]

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

        new_client_ip = f"10.8.0.{new_client_ip_index}"

        return new_client_ip


class AddClientCommand:
    def generate_private_key(self):
        print("Generating new private key...")

        client_index = NameParser.parse_filename()
        new_private_key_path = f"{WG_DIR}client{client_index}_private.key"

        result = subprocess.run(
            ["wg", "genkey"], capture_output=True, check=True, text=True
        )

        client_private_key = result.stdout.strip()

        with open(new_private_key_path, "w") as f:
            f.write(client_private_key)

        print("Private key generated")

        self.generate_public_key(client_private_key, client_index)

    def generate_public_key(self, client_private_key, client_index):
        new_public_key_path = f"{WG_DIR}client{client_index}_public.key"

        print("Generating new public key...")

        result = subprocess.run(
            ["wg", "pubkey"],
            input=client_private_key,
            check=True,
            capture_output=True,
            text=True,
        )

        client_public_key = result.stdout.strip()

        with open(new_public_key_path, "w") as f:
            f.write(client_public_key)

        print("Public key generated")

        self.create_client_config(client_public_key, client_private_key, client_index)

    def create_client_config(self, client_public_key, client_private_key, client_index):
        print("Creating new client config file...")

        new_client_config_path = f"{WG_DIR}client{client_index}.conf"

        server_public_key_path = f"{WG_DIR}server_public.key"

        new_client_ip = NameParser.parse_ip()

        cmd = "ip addr show ens3 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        server_ip = result.stdout.strip()

        with open(server_public_key_path, "r") as f:
            server_public_key = f.read().strip()

        config = f"""[Interface]
PrivateKey = {client_private_key}
Address = {new_client_ip}/24
DNS = 8.8.8.8
[Peer]
PublicKey = {server_public_key}
AllowedIPs = 0.0.0.0/0
Endpoint = {server_ip}:51820
PersistentKeepalive = 15
"""

        with open(new_client_config_path, "w") as f:
            f.write(config)

        self.add_peer_to_server_config(client_public_key, new_client_ip)

    def add_peer_to_server_config(self, client_public_key, new_client_ip):
        print("Adding new client to server config")

        peer_block = f"\n[Peer]\nPublicKey = {client_public_key}\nAllowedIPs = {new_client_ip}/32\n"

        with open(WG_SERVER_CONFIG_PATH, "a") as f:
            f.write(peer_block)

        print("DONE! New client successfully added")
