from eip712_structs import EIP712Struct, Address, Uint


class Order(EIP712Struct):
    sender = Address()
    size = Uint(128)
    price = Uint(128)
    nonce = Uint(64)
    productIndex = Uint(8)
    orderSide = Uint(8)


