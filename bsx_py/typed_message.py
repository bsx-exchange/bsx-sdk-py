from eth_account.signers.local import LocalAccount

from .helper.chain_info import get_chain_config
from .instance import Environment


def gen_register_typed_message_for_smart_contract(env: Environment | str, signer: LocalAccount, nonce: int) -> dict:
    """
    Helper function to generate the typed message that used to generate the signature for register a smart contract.

    Note that this function should only be used to get the data of the typed message.
    The way to construct the message depends on the language that is used to generate the signature.

    Attributes:
        env (Environment|str): environment to use (Testnet or mainnet) or the domain in plain text

        signer (LocalAccount): signer wallet used to sign requests

        nonce (int): nonce that will be used to call the register API. We recommend using current timestamp in nanoseconds.
        Nonce should be unique across all requests of a user

    Return:
        dict: typed message in dict format.
    """
    domain = env.value if isinstance(env, Environment) else env
    config = get_chain_config(domain)
    return {
        "types": {
            "EIP712Domain": [
                {
                    "name": 'name',
                    "type": 'string'
                },
                {
                    "name": 'version',
                    "type": 'string'
                },
                {
                    "name": 'chainId',
                    "type": 'uint256'
                },
                {
                    "name": 'verifyingContract',
                    "type": 'address'
                }
            ],
            "Register": [
                {
                    "name": 'key',
                    "type": 'address'
                },
                {
                    "name": 'message',
                    "type": 'string'
                },
                {
                    "name": 'nonce',
                    "type": 'uint64'
                }
            ]
        },
        "primaryType": 'Register',
        "domain": {
            "name": config["name"],
            "version": config["version"],
            "chainId": config["chain_id"],
            "verifyingContract": config["verifying_contract"]
        },
        "message": {
            "key": signer.address,
            "message": 'Please sign in with your wallet to access bsx.exchange. You are signing in on %d. '
                       'This message is exclusively signed with bsx.exchange for security.' % nonce,
            "nonce": str(nonce)
        }
    }
