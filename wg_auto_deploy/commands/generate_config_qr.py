import subprocess, os

from . import config

class QRGenerator():
    def generate_config_qr(self, client_name):
        client_path = f"{config.WG_DIR}{client_name}.conf"
        
        if(os.path.exists(client_path)):
            with open(client_path, "r") as f:
                subprocess.run(["qrencode", "-t", "ansiutf8"], input=f.read() , text=True, check=True)
        else:
            print(f"Error: client {client_name} config not found in WG directory")
