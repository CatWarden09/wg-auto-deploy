import argparse
from .commands import AddClientCommand, QRGenerator

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_client_parser = subparsers.add_parser("add-client")

    qr_gen_parser = subparsers.add_parser("qr-gen")
    qr_gen_parser.add_argument("client_name") 

    args = parser.parse_args()


    if args.command == "add-client":
        add_cmd = AddClientCommand()
        add_cmd.run()

    if args.command == "qr-gen":
        qr_generator = QRGenerator()
        qr_generator.generate_config_qr(args.client_name)