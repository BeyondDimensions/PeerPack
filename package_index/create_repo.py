import walytis_beta_api as wapi


def create_repo(repo_name: str):
    return wapi.Blockchain.create(blockchain_name=f"PeerPack-{repo_name}")
