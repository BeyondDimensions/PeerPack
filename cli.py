from utils.logger import logger
import argparse
import peerpack_api


def main():
    parser = argparse.ArgumentParser(
        description='It is a CLI-Frontend for the decentralzised package peerpack_api Peer Pack')

    subparser = parser.add_subparsers(dest='command', required=True, help='Available commands')

    # Command to list the available packages
    list_parser = subparser.add_parser('list', help='Lists the available packages')
    list_parser.add_argument('repository_package', type=str,
                             help='Name of the repository to list the packages from (Format: repository.package)')

    # Command to install the latest version
    install_parser = subparser.add_parser('install', help='Installs the package')
    install_parser.add_argument('repository_package', type=str,
                                help='Name of the package to install (Format: repository.package)')
    install_parser.add_argument('--version', type=str, help='Version of the package')

    # Command to update the packege
    update_parser = subparser.add_parser('update', help='Updates the package')
    update_parser.add_argument('repository_package', type=str,
                               help='Name of the package to update (Format: repository.package)')

    # Command to unisntall the packages
    uninstall_parser = subparser.add_parser('uninstall', help='Uninstalls the package')
    uninstall_parser.add_argument('package', type=str, help='Name of the package to uninstall')

    # Command to check the version of the package
    version_parser = subparser.add_parser('version', help='Checks the version of the package')
    version_parser.add_argument(
        'package', type=str, help='Name of the package to check the version')

    # Command to register a package
    register_parser = subparser.add_parser('register', help='Registers a package')
    register_parser.add_argument('repository_package', type=str,
                                 help='Name of the package to register (Format: repository.package)')
    register_parser.add_argument('--description', type=str, help='Description of the package')

    # Command to release/publish a package
    release_parser = subparser.add_parser(
        'release', help='Push the registered package to a repository')
    release_parser.add_argument('repository_package', type=str,
                                help='Name of the package to release (Format: repository.package)')
    release_parser.add_argument('--version', type=str, required=True,
                                help='Version of the package being released')
    release_parser.add_argument('--file', type=str, required=True, help='Path to the file')
    release_parser.add_argument('--key', type=str, required=True,
                                help='Private key for authenticating releases')

    args = parser.parse_args()

    if args.command == 'list':
        repo, package = args.repository_package.split('.')
        peerpack_api.list_package(package, repo)

    elif args.command == 'install':
        repo, package = args.repository_package.split('.')
        peerpack_api.install_package(package, args.version, repo)

    elif args.command == 'update':
        repo, package = args.repository_package.split('.')
        peerpack_api.update_package(package, repo)

    elif args.command == 'uninstall':
        peerpack_api.update_package(args.uninstall)

    elif args.command == 'version':
        peerpack_api.get_package_version(args.version)

    elif args.command == 'register':
        repo, package = args.repository_package.split('.')
        private_key = peerpack_api.register_package(package, repo, args.description)
        print("Here is your private key for managing this package:")
        print(private_key)

    elif args.command == 'release':
        repo, package = args.repository_package.split('.')
        peerpack_api.release_package(package, args.version, args.file, repo, args.key)


if __name__ == "__main__":
    main()
else:
    print("---------- CLI TESTS --------------")
    import os
    import sys
    sys.path.insert(0, (os.path.dirname(__file__)))
    from tests import dummy_peerpack_api as peerpack_api
    main()
