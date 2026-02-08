import argparse
from commands import AddClientCommand

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["add-client"])
    args = parser.parse_args()

    if args.action == "add-client":
        add_cmd = AddClientCommand()
        add_cmd.generate_private_key()