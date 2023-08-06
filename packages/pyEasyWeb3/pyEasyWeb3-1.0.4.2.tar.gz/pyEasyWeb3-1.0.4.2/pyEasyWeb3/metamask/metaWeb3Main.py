from secrets import token_hex

from eth_account import Account
from pyEasyWeb3 import web3ConnectionError
from .metaWeb3Abi import abi
from .metaWeb3DataType import dataTypeClass
from web3 import Web3


class metaWeb3:
    def __init__(self, httpProvider:str='https://bsc-dataseed1.binance.org/') -> None:
        '''
        take: httpProvider (default network bsc).
        '''
        self.w3 = Web3(Web3.HTTPProvider(httpProvider))
        if self.w3.isConnected() == True:print('Web3 is connected: True')
        else:raise web3ConnectionError(httpProvider)

    def createWallet(self) -> dataTypeClass.createWallet:
        '''
        Create a new private key.
        '''
        return dataTypeClass.createWallet(privateKey="0x" + token_hex(32))

    def createWalletWithMnemonic(self) -> dataTypeClass.createWalletWithMnemonic:
        '''
        Create a new private key and mnemonic.
        '''
        Account.enable_unaudited_hdwallet_features()
        acct, mnemonic = Account.create_with_mnemonic()
        return dataTypeClass.createWalletWithMnemonic(address=acct.address,privateKey=acct.key.hex(),mnemonic=mnemonic)

    def getWalletAddress(self,privateKey:str) -> dataTypeClass.getWalletAddress:
        '''
        Gets the account address.
        take: your private key.
        '''
        return dataTypeClass.getWalletAddress(privateKey=privateKey,address=Account.from_key(privateKey).address)

    def getBalanceWallet(self,address:str, contractAddressToken:str=None) -> dataTypeClass.getBalanceWallet:
        '''
        Gets network token or contract token balance.
        take: your address (if you want to get a network token: etc, bnb, matic and others) or your address and contract address token (if you want to get any other token: usdt, cake, twt and others).
        '''
        try:
            if contractAddressToken == None:
                return dataTypeClass.getBalanceWallet(address=address,balance=float(self.w3.fromWei(self.w3.eth.getBalance(address),"ether")))
            elif contractAddressToken != None:
                instance = self.w3.eth.contract(address=Web3.toChecksumAddress(contractAddressToken),abi = abi.balanceAbi)
                return dataTypeClass.getBalanceWallet(address=address,balance=float(self.w3.fromWei(instance.functions.balanceOf(address).call(),"ether")))
        except Exception as e:return dataTypeClass.getBalanceWallet(address=address,balance=0.0,error=f'{e}')
    
    def getNonce(self, address:str) -> dataTypeClass.getNonce:
        '''
        Gets the transaction number.
        '''
        return dataTypeClass.getNonce(address=address,nonce=self.w3.eth.getTransactionCount(address))

    def transferToken(self,privateKey:str, addressTo:str, qty:int=0, contractAddressToken:str=None, transferAll:bool=False, threadingNum:int=0, userNonce:int=None) -> dataTypeClass.transferToken:
        '''
        Sends tokens.
        take: your private key, where to send, qty of tokens (If you want to send a certain quantity), contract address token (if you want to send a non-network token), transferAll (if you want to send all tokens).\n
        other: threadingNum, each transaction has a number, and if you send several transactions at once, one of them will not be sent, because it will have the same number as the previous one, by passing the number to this variable, you add some number to the current transaction: transferToken(), transferToken() = successful,error || transferToken(), transferToken(threadingNum=1) = successful,successful.\n
        userNonce, you can specify the transaction number yourself.
        '''
        try:
            mainAddress = self.getWalletAddress(privateKey=privateKey).address

            if userNonce == None:
                nonce = self.w3.eth.getTransactionCount(mainAddress)+threadingNum
            else:
                nonce = userNonce
            if contractAddressToken != None:
                contract = self.w3.eth.contract(address=contractAddressToken, abi=abi.transferAbi)       
                if transferAll == False:
                    balanceTtansfer = self.w3.toWei(qty,'ether')
                elif transferAll == True:
                    balanceTtansfer =  self.w3.toWei(self.getBalanceWallet(address=mainAddress, contractAddressToken=contractAddressToken).balance*.99999,'ether')
                tokenTxn = contract.functions.transfer(
                    addressTo,
                    balanceTtansfer,
                ).buildTransaction({
                    "from": mainAddress,
                    'nonce': nonce,
                    'gasPrice': self.w3.eth.gas_price
                })
                signed_txn = self.w3.eth.account.signTransaction(tokenTxn, privateKey)

            elif contractAddressToken == None:
                contract = self.w3.eth.contract(address=addressTo, abi=abi.transferAbi)
                if transferAll == False:
                    valueTransfer = self.w3.toWei(qty,'ether')
                elif transferAll == True:
                    valueTransfer = self.w3.toWei(self.getBalanceWallet(address=mainAddress).balance*.99999-(float(self.w3.fromWei(self.w3.eth.gas_price,"ether"))*21560), 'ether')
                tokenTxn = contract.functions.transfer(
                    addressTo,
                    1,
                ).buildTransaction({
                    'nonce': nonce,
                    'value': valueTransfer,
                    'gasPrice': self.w3.eth.gas_price
                })
                signed_txn = self.w3.eth.account.signTransaction(tokenTxn, privateKey)
            return dataTypeClass.transferToken(transactionHash=f'{self.w3.toHex(self.w3.eth.sendRawTransaction(signed_txn.rawTransaction))}')
        except Exception as e:return dataTypeClass.transferToken(transactionHash='', error=f'{e}')