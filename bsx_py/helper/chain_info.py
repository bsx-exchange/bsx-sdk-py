import requests


def get_chain_config(domain: str):
    response = requests.get(domain + "/chain/configs")
    if response.status_code != 200:
        raise Exception(
            f"Failed to get chain config. Response code: {response.status_code}. "
            f"Response: {response.text}"
        )

    return response.json()
