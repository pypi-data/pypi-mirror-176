from typing import NamedTuple

class dataTypeClass:
    class createWallet(NamedTuple):
        privateKey:str

    class createWalletWithMnemonic(NamedTuple):
        address:str
        privateKey:str
        mnemonic:str

    class getWalletAddress(NamedTuple):
        privateKey:str
        address:str

    class getBalanceWallets(NamedTuple):
        privateKey:str
        address:str

    class getBalanceWallet(NamedTuple):
        address:str
        balance:float
        error:str=None

    class getNonce(NamedTuple):
        address:str
        nonce:int
        
    class transferToken(NamedTuple):
        transactionHash:str
        error:str=None