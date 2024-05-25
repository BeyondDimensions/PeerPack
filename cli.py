import argparse
from peerpack import manager

def main():
    parse = argparse.ArgumentParser(descrition='It is a CLi-Frontend for the decentralzised package manager Peer Pack')

    subparser = parser.add_subparsers(dest='command', required=True, help='Available commands')

    # Command to install the latest version
    install_parser = subparser.add_parser('install', help='Installs the package')
