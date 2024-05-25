import ipfs_api
import json
import walytis_beta_api as wapi
from cryptem import Crypt
from .exceptions import (
    PackageExistsError, NoSuchPackageError, InvalidBlockError,
    VersionIsntGreaterError
)
from utils.logger import logger
from brenthy_tools_beta.utils import (bytes_to_string, string_to_bytes)
from brenthy_tools_beta.version_utils import is_version_greater

import json
import jsonschema
from jsonschema import validate
import tempfile
import os

# Load the package block data formats from a file
REG_SCH_PATH = os.path.join(os.path.dirname(__file__), 'registration_schema.json')
REL_SCH_PATH = os.path.join(os.path.dirname(__file__), 'release_schema.json')
with open(REG_SCH_PATH, 'r') as schema_file:
    REGISTRATION_SCHEMA = json.load(schema_file)
with open(REL_SCH_PATH, 'r') as schema_file:
    REGISTRATION_SCHEMA = json.load(schema_file)

REGISTER_TOPIC = "package_registration"
RELEASE_TOPIC = "package_release"


class PackageRepo:
    def __init__(self, repo_name: str):
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
            "package_name": package_name,
            "public_key": public_key
        }
        self.blockchain.add_block(
            json.dumps(block_content).encode(),
            topics=[REGISTER_TOPIC, package_name]
        )

        return private_key

    def release_package(
        self,
        package_name: str,
        version: str,
        dependencies: list[tuple[str, str, bool]],
        package_data: str,
        key: str
    ):
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
            "package_name": package_name,
            "version": version,
            "public_key": public_key,
            "package_data": ipfs_api.publish(package_data)
        }

        # sign data and append the signature
        signature = crypt.sign(json.dumps(block_content).encode())
        block_content.update({"signature": bytes_to_string(signature)})

        self.blockchain.add_block(
            json.dumps(block_content).encode(),
            topics=[REGISTER_TOPIC, package_name]
        )

    def list_packages(self) -> list[str]:
        """Get a list of the available packages.

        Returns:
            list[str]: a list of package names
        """
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
        """Get the available versions of the specified packaged
        """
        return [
            release["version"]
            for release in self._get_package_releases(package_name)
        ]

    def get_package_dependencies(
        self, package_name: str, version: str
    ) -> list[tuple[str, str, bool]]:
        """Get the dependencies of the specified version of the package.

        Returns:
            list[tuple[str, str, bool]]: the dependencies
                str: package name
                str: version
                bool: whether this specific version is required, or newer
                    versions can be used as well
        """
        release = self._get_package_release(self, package_name, version)
        return release["dependencies"]

    def download_package(self, package_name: str, version: str | None) -> str:
        """Download a specific version of a package.

        Returns:
            str: the download location of the installable package data
        """
        if not version:
            release = self._get_package_releases(package_name)[-1]
        else:
            release = self._get_package_release(package_name, version)

        tempdir = tempfile.mkdtemp()
        download_path = os.path.join(tempdir, package_name)
        ipfs_api.download(release["ipfs_cid"])
        return download_path

    def _get_package_release(self, package_name: str, version: str) -> dict:
        """Get the release metadata of this version of the package."""
        # search for the desired release
        release = [
            release for release in self._get_package_releases(package_name)
            if release["version"] == version
        ]
        if not release:
            raise VersionNotFoundError()
        if len(releases) > 1:
            raise NotSupposedToHappenError()
        return release[0]

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
