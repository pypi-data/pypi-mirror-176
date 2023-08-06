from concurrent.futures import ThreadPoolExecutor, as_completed

from .metaWeb3DataType import dataTypeClass
from .metaWeb3Main import metaWeb3


class metaWeb3Threading:
    '''
    take: maxWorkers (by default, without restrictions), httpProvider (default network bsc).
    '''
    def __init__(self,maxWorkers:int=None, httpProvider:str='https://bsc-dataseed1.binance.org/') -> None:
        self.targetClass = metaWeb3(httpProvider=httpProvider)
        self.maxWorkers = maxWorkers

    def createWalletThreading(self, qty:int) -> list[dataTypeClass.createWallet]:
        with ThreadPoolExecutor(max_workers=self.maxWorkers) as executor:
            futures = [executor.submit(self.targetClass.createWallet) for _ in range(qty)] 
        return [future.result() for future in as_completed(futures)]

    def getWalletAddressThreading(self, privateKeys:list[str]) -> list[dataTypeClass.getWalletAddress]:
        with ThreadPoolExecutor(max_workers=self.maxWorkers) as executor:
            futures = [executor.submit(self.targetClass.getWalletAddress, privateKey=privateKey) for privateKey in privateKeys] 
        return [future.result() for future in as_completed(futures)]
    
    def createWalletWithMnemonicThreading(self, qty:int) -> list[dataTypeClass.createWalletWithMnemonic]:
        with ThreadPoolExecutor(max_workers=self.maxWorkers) as executor:
            futures = [executor.submit(self.targetClass.createWalletWithMnemonic) for _ in range(qty)]
        return [future.result() for future in as_completed(futures)]

    def getNonceThreading(self, addressList:list[str]) -> list[dataTypeClass.getNonce]:
        with ThreadPoolExecutor(max_workers=self.maxWorkers) as executor:
            futures = [executor.submit(self.targetClass.getNonce, address=address) for address in addressList] 
        return [future.result() for future in as_completed(futures)]

    def getBalanceWalletThreading(self, addressList:list[str], contractAddressToken:str=None) -> list[dataTypeClass.getBalanceWallet]:
        with ThreadPoolExecutor(max_workers=self.maxWorkers) as executor:
            futures = [executor.submit(self.targetClass.getBalanceWallet, address=address, contractAddressToken=contractAddressToken) for address in addressList] 
        return [future.result() for future in as_completed(futures)]