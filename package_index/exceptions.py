class PackageExistsError(Exception):
    """When a package already exists."""


class NoSuchPackageError(Exception):
    """When a package doesn't exist."""


class InvalidBlockError(Exception):
    """When a block's content & topics block don't conform to a format."""


class ReleaseKeyError(Exception):
    """When the provided private key for publishing releases isn't correct"""


class VersionIsntGreaterError(Exception):
    """When a provided package version is too low."""


class VersionNotFoundError(Exception):
    """When the provided version couldn't be found for the specified package."""


class NotSupposedToHappenError(Exception):
    """Indicate bugs."""
