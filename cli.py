import argparse
from peerpack import manager

def main():
    parse = argparse.ArgumentParser(description='It is a CLI-Frontend for the decentralzised package manager Peer Pack')

    subparser = parser.add_subparsers(dest='command', required=True, help='Available commands')

    # Command to list the available packages
    list_parser = subparsers.add_parser('list', help='Lists the available packages')
    list_parser.add_argument('repository.package', type=str, help='Name of the repository to list the packages from')

    # Command to install the latest version
    install_parser = subparser.add_parser('install', help='Installs the package')
    install_parser.add_argument('repository.package', type=str, help='Name of the package to install')
    install_parser.add_argument('--version', type=str, help='Version of the package')

    # Command to update the packege
    update_parser = subparser.add_parser('update', help='Updates the package')
    update_parser.add_argument ('repository.package', type=str, help='Name of the package to update')

    # Command to unisntall the packages
    uninstall_parser = subparser.add_parser('update', help='Uninstalls the package')
    uninstall_parser.add_argument ('package', type=str, help='Name of the package to uninstall')

    #Command to check the version of the package
    version_parser = subparser.add_parser('update', help='Checks the version of the package')
    version_parser.add_argument ('package', type=str, help='Name of the package to check the version')

    # Command to register a package
    register_parser = subparser.add_parser('register', help='Registers a package')
    register_parser.add_argument ('repository.package', type=str, help='Name of the package to register')
    register_parser.add_argument ('--version', type=str, required=True, help='Version of the package being registered')
    register_parser.add_argument ('--description', type=str, help='Description of the package')

    # Command to release/publish a package
    release_parser = subparser.add_parser('repository.release', help='Push the registered package to a repository')
    release_parser.add_argument ('repository.package', type=str, help='Name of the package to release')
    release_parser.add_argument ('--version', type=str, required=True, help='Version of the package being released')
    release_parser.add_argument ('--file', type=str, required=True, help='Path to the file')

    args = parser.parse_args()

    if args.command == 'list':
        manager.list_packages()

    elif args.command == 'install':
        manager.install_package(args.package, args.version)

    elif args.command == 'update':
        manager.update_package(args.update)

    elif args.command == 'uninstall':
        manager.update_package(args.uninstall)

    elif args.command == 'version':
        manager.update_package(args.version)

if __name__ == "__main__":
    main()
