from tronpy import Tron


def get_wallet_info(address: str) -> dict:
    client = Tron()
    acc = client.get_account(address)

    bandwidth = client.get_account_resource(address)["free_net_limit"]
    energy = client.get_account_resource(address)["energy_limit"]

    return {
        "address": address,
        "bandwidth": bandwidth,
        "energy": energy,
        "balance": acc.get("balance", 0) / 1_000_000
    }
