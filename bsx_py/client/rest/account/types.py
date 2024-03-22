from eip712_structs import EIP712Struct, Address, String, Uint


class SignKey(EIP712Struct):
    account = Address()


class Register(EIP712Struct):
    key = Address()
    message = String()
    nonce = Uint(64)


class Withdraw(EIP712Struct):
    sender = Address()
    token = Address()
    amount = Uint(128)
    nonce = Uint(64)
