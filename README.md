# Description
A small script for server-side WireGuard configs automation

# Requirements
- Ubuntu 22+ (versions <22 might work but require different installation approach)
- pipx
- prepared WireGuard server config (.conf file, public and private server keys). Currently the script uses the hardcoded file system, future versions will allow full server setup from scratch.
  
```bash
sudo apt install -y pipx
sudo pipx ensurepath
```

- qrencode
```bash
sudo apt install -y qrencode
```

# Installation
```bash
git clone https://github.com/CatWarden09/wg-auto-deploy.git
cd wg-auto-deploy
pipx install .
```

# Usage
1. ```wg_auto_deploy add-client``` - this command generates a pair of public/private keys and a config file for the client. The clients name are generated sequentially (like client1, client2 etc.)
2. ```wg-auto-deploy qr-gen [client-name]``` - this command accepts client name as an argument, looks for the .conf file in the WireGuard directory by the given name and prints the QR-code for this config. It can be scanned by WireGuard mobile app to set up a tunnel. **WARNING!** - client name should be passed without the file format.
