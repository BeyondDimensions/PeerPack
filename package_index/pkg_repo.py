import ipfs_api
import json
import walytis_beta_api as wapi
from cryptem import Crypt
from .exceptions import (
    PackageExistsError, NoSuchPackageError, InvalidBlockError,
    VersionIsntGreaterError
)
import loguru
from brenthy_tools_beta.utils import (bytes_to_string, string_to_bytes)
from brenthy_tools_beta.version_utils import is_version_greater

import json
import jsonschema
from jsonschema import validate


# Load the package block data formats from a file
with open('registration_schema.json', 'r') as schema_file:
    REGISTRATION_SCHEMA = json.load(schema_file)
with open('release_schema.json', 'r') as schema_file:
    REGISTRATION_SCHEMA = json.load(schema_file)

REGISTER_TOPIC = "package_registration"
RELEASE_TOPIC = "package_release"


class PackageRepo:
    def __init__(self, repo_name):
        self.blockchain = wapi.Blockchain(f"PeerPack-{repo_name}")

    def register_package(self, package_name, version: str) -> str:
        """Register a new package.

        Returns:
            The private key to publishing this package.
        """
        if package_name in self.list_packages():
            raise PackageExistsError()
        crypt = Crypt()
        private_key = crypt.get_private_key()
        public_key = crypt.get_public_key()

        block_content = {
            "package_name" = package_name,
            "public_key" = public_key
        }
        self.blockchain.add_block(
            json.dumps(block_content).encode(),
            topics=[REGISTER_TOPIC, package_name]
        )

        return private_key

    def release_package(self, package_name: str, version: str, package_data: str, key: str):
        """Publish a new version of a package."""
        if not is_version_greater(version, self.get_package_versions(package_name[-1])):
            raise VersionIsntGreaterError()
        crypt = Crypt(private_key=private_key)

        if (
                crypt.get_public_key()
                != self._get_package_registration(package_name)["public_key"]
        ):
            raise ReleaseKeyError()

        block_content = {
            "package_name" = package_name,
            "version": version,
            "public_key" = public_key,
            "package_data" = ipfs_api.publish(package_data)
        }

        # sign data and append the signature
        signature = crypt.sign(json.dumps(block_content).encode())
        block_content.update({"signature": bytes_to_string(signature)})

        self.blockchain.add_block(
            json.dumps(block_content).encode(),
            topics=[REGISTER_TOPIC, package_name]
        )

    def list_packages(self) -> list[str]:
        """Get a list of the available packages."""
        registration_blocks = [
            block_id for block_id in self.blockchain.block_ids
            if REGISTER_TOPIC in wapi.decode_short_id(block_id).topics
        ]

        package_names = []
        for block in registration_blocks:
            try:
                self._read_registration_block(block)
            except Exception as error:
                loguru.warning(f"Found corrupt registration_block:\n{error}")
        return package_names

    def get_package_versions(self, package_name: str) -> list[str]:
        return [
            release["version"]
            for release self._get_package_releases(package_name)
        ]

    def _get_package_releases(self, package_name: str) -> list[dict]:
        """Get the available package versions for a given package"""
        package_registration = self._get_package_registration(package_name)
        releases = []
        for block_id in self.blockchain.block_ids:
            if (RELEASE_TOPIC in wapi.decode_short_id(block_id).topics
                    and package_name in wapi.decode_short_id(block_id).topics
                ):
                try:
                    releases.append(self._read_release_block(
                        self.blockchain.get_block(block_id)))
                except Exception as error:
                    loguru.warning(error)

    def download_package(self, package_name: str, version: str) -> str:
        """Download a specific version of a package.

        Returns:
            str: the download location
        """
        pass

    def _get_package_registration(self, package_name: str) -> dict | None:
        """Get the contents of the initial package registration block."""
        for block_id in self.blockchain.block_ids:
            if (REGISTER_TOPIC in wapi.decode_short_id(block_id).topics
                    and package_name in wapi.decode_short_id(block_id).topics
                ):
                try:
                    return self._read_registration_block(self.blockchain.get_block(block_id))
                except Exception as error:
                    loguru.warning(error)

    def _read_registration_block(self, block) -> dict:
        """Load package registration data from a block."""
        try:
            registration_data = json.loads(block.content.decode())
            validate(instance=package, schema=REGISTRATION_SCHEMA)
            assert registration_data["package_name"] in block.topics
            assert REGISTER_TOPIC in block.topics
        except:
            raise InvalidBlockError()
        return registration_data

    def _read_release_block(self, block) -> dict:
        """Load package release data from a block."""
        try:
            registration_data = json.loads(block.content.decode())
            validate(instance=package, schema=RELEASE_SCHEMA)
            assert registration_data["package_name"] in block.topics
            assert RELEASE_TOPIC in block.topics
        except:
            raise InvalidBlockError()
        return registration_data
