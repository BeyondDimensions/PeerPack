register_package(self, package_name, version: str) -> str

release_package(self, package_name: str, version: str, package_data: str, key: str)

list_packages(self) -> list[str]

get_package_versions(self, package_name: str) -> list[str]

download_package(self, package_name: str, version: str | None) -> str
