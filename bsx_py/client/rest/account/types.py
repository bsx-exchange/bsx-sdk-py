from eip712_structs import EIP712Struct, Address, Uint


class Withdraw(EIP712Struct):
    sender = Address()
    token = Address()
    amount = Uint(128)
    nonce = Uint(64)
