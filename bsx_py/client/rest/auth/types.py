from eip712_structs import EIP712Struct, Address, Uint, String


class SignKey(EIP712Struct):
    account = Address()


class Register(EIP712Struct):
    key = Address()
    message = String()
    nonce = Uint(64)
