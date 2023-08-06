
# **pyEasyWeb3**

library for easy web3 usage (*default network **BSC***)


## **Features**

- Creating a wallet
- Creating a wallet with mnemonic
- Get wallet address
- Get wallet balance
- Get nonce
- Sending transactions
- write/read xlsx file



## **Installation**
```python
pip install pyEasyWeb3
```
If you have such an error during installation, install the Microsoft C++ Build Tools with ***Desktop Development using C++***

![image description](https://cdn.discordapp.com/attachments/1041747038741745776/1041840211086286938/image.png)
 
## **Library classes**
Class | Variables | Functions
:---: | --- | ---
*metaWeb3* | **httpProvider**:str|*createWallet*, *createWalletWithMnemonic*, *getWalletAddress*, *getBalanceWallet*, *getNonce*, *transferToken*
*metaWeb3Threading* | **maxWorkers**:int, **httpProvider**:str|*createWalletThreading*, *getWalletAddressThreading*, *createWalletWithMnemonicThreading*, *getNonceThreading*, *getBalanceWalletThreading*
*metaWeb3AsyncDef* | **httpProvider**:str|*createWallet*, *createWalletWithMnemonic*, *getWalletAddress*, *getBalanceWallet*, *getNonce*, *transferToken*
*metaWeb3Async* | **httpProvider**:str|*createWalletAsync*, *getWalletAddressAsync*, *createWalletWithMnemonicAsync*, *getNonceAsync*, *getBalanceWalletAsync*
*exelData* |~~None~~|*listNamedTupleToXlsx*, *readXlsxFile*

## **metaWeb3**
Function | Variables | #
:---: | --- | ---
*createWallet* | ~~None~~|Create a new private key.
*createWalletWithMnemonic* |~~None~~|Create a new private key and mnemonic.
*getWalletAddress* | **privateKey**:str|Gets the account address.
*getBalanceWallet* | **address**:str, **contractAddressToken**:str| Gets network token or contract token balance.
*getNonce* | **address**:str|Gets the transaction number
*transferToken* | **privateKey**:str, **addressTo**:str, **qty**:int, **contractAddressToken**:str, **transferAll**:bool, **threadingNum**:int, **userNonce**:int|Sends tokens.

```python
from pyEasyWeb3 import metaWeb3

def testMetaWeb3():
    metaw3BSC = metaWeb3() # network BSC
    metaw3POLYGON = metaWeb3(httpProvider='https://polygon-rpc.com/') # network polygon

    newPrivateKey = metaw3BSC.createWallet()

    newWalletWithMnemonic = metaw3BSC.createWalletWithMnemonic()

    addressWallet = metaw3BSC.getWalletAddress(privateKey=newPrivateKey.privateKey)

    balanceWallet = metaw3BSC.getBalanceWallet(address=addressWallet.address) # bnb 
    balanceWalletContractToken = metaw3BSC.getBalanceWallet(address=addressWallet.address, contractAddressToken='0x55d398326f99059ff775485246999027b3197955') # contract usdt (bsc network)

    nonce = metaw3BSC.getNonce(address=addressWallet.address)

    # transactions will be with errors since there are no tokens on wallets

    transferBnb = metaw3BSC.transferToken(privateKey=newPrivateKey.privateKey, addressTo=newWalletWithMnemonic.address, qty=0.01) # send 0.01 bnb
    transferBnbAll = metaw3BSC.transferToken(privateKey=newPrivateKey.privateKey, addressTo=newWalletWithMnemonic.address, transferAll=True, threadingNum=1) #send all bnb | threadingNum, 
    
    #each transaction has a number, and if you send several transactions at once, one of them will not be sent, because it will have the same number as the previous one, by passing the number 
    # to this variable, you add some number to the current transaction: transferToken(), transferToken() = successful,error || transferToken(), transferToken(threadingNum=1) = successful,successful. 
    
    nonceTransferUsdt = metaw3BSC.getNonce(address=addressWallet.address)
    transferUSDT = metaw3BSC.transferToken(privateKey=newPrivateKey.privateKey, addressTo=newWalletWithMnemonic.address, contractAddressToken= '0x55d398326f99059ff775485246999027b3197955', qty=0.01, userNonce=nonceTransferUsdt.nonce)# send 0.01 usdt
    
    # userNonce, you can specify the transaction number yourself.
    
    transferUsdtAll = metaw3BSC.transferToken(privateKey=newPrivateKey.privateKey, addressTo=newWalletWithMnemonic.address, contractAddressToken= '0x55d398326f99059ff775485246999027b3197955', transferAll=True, userNonce=nonceTransferUsdt.nonce+1)# send all usdt

    print(f"{newPrivateKey=}\n{newWalletWithMnemonic=}\n{addressWallet=}\n{balanceWallet=}\n{balanceWalletContractToken=}\n{nonce=}\n{transferBnb=}\n{transferBnbAll=}\n{transferUSDT=}\n{transferUsdtAll=}")

if __name__ == '__main__':
    testMetaWeb3()
```
![](https://s4.gifyu.com/images/gif121.gif)

## **metaWeb3Threading**
Function | Variables | #
:---: | --- | ---
*createWalletThreading* | **qty**:int|Create a new private key.
*getWalletAddressThreading* |**privateKeys**:list[str]|Gets the account address.
*createWalletWithMnemonicThreading* | **qty**:int|Create a new private key and mnemonic.
*getNonceThreading* |**addressList**:list[str]|Gets the transaction number 
*getBalanceWalletThreading* | **addressList**:list[str], **contractAddress**:str|Gets network token or contract token balance.


```python
from pyEasyWeb3 import metaWeb3Threading

def testMetaWeb3():
    metaw3BSC = metaWeb3Threading() # network BSC

    newPrivateKey = metaw3BSC.createWalletThreading(qty=10)

    newWalletWithMnemonic = metaw3BSC.createWalletWithMnemonicThreading(qty=10)

    addressWallet = metaw3BSC.getWalletAddressThreading(privateKeys=[key.privateKey for key in newPrivateKey])
    addressList = [address.address for address in addressWallet]

    balanceWallet = metaw3BSC.getBalanceWalletThreading(addressList=addressList) # bnb 
    balanceWalletContractToken = metaw3BSC.getBalanceWalletThreading(addressList=addressList, contractAddressToken='0x55d398326f99059ff775485246999027b3197955') # contract usdt (bsc network)

    nonce = metaw3BSC.getNonceThreading(addressList=addressList)

    print(f"{newPrivateKey=}\n{newWalletWithMnemonic=}\n{addressWallet=}\n{balanceWallet=}\n{balanceWalletContractToken=}\n{nonce=}")

if __name__ == '__main__':
    testMetaWeb3()
```
![](https://cdn.discordapp.com/attachments/1041747038741745776/1041756471089692692/2022-11-14-19-11-08_1__1_.gif)

## **metaWeb3AsyncDef**
Function | Variables | #
:---: | --- | ---
*createWallet* | ~~None~~|Create a new private key.
*createWalletWithMnemonic* |~~None~~|Create a new private key and mnemonic.
*getWalletAddress* | **privateKey**:str|Gets the account address.
*getBalanceWallet* | **address**:str, **contractAddressToken**:str| Gets network token or contract token balance.
*getNonce* | **address**:str|Gets the transaction number
*transferToken* | **privateKey**:str, **addressTo**:str, **qty**:int, **contractAddressToken**:str, **transferAll**:bool, **threadingNum**:int, **userNonce**:int|Sends tokens.

```python
from pyEasyWeb3 import metaWeb3AsyncDef
from asyncio import run

async def testMetaWeb3():
    metaw3BSC = metaWeb3AsyncDef() # network BSC

    newPrivateKey = await metaw3BSC.createWallet()

    newWalletWithMnemonic = await metaw3BSC.createWalletWithMnemonic()

    addressWallet = await metaw3BSC.getWalletAddress(privateKey=newPrivateKey.privateKey)

    balanceWallet = await metaw3BSC.getBalanceWallet(address=addressWallet.address) # bnb 
    balanceWalletContractToken = await metaw3BSC.getBalanceWallet(address=addressWallet.address, contractAddressToken='0x55d398326f99059ff775485246999027b3197955') # contract usdt (bsc network)

    nonce = await metaw3BSC.getNonce(address=addressWallet.address)

    # transactions will be with errors since there are no tokens on wallets

    transferBnb = await metaw3BSC.transferToken(privateKey=newPrivateKey.privateKey, addressTo=newWalletWithMnemonic.address, qty=0.01) # send 0.01 bnb
    transferBnbAll = await metaw3BSC.transferToken(privateKey=newPrivateKey.privateKey, addressTo=newWalletWithMnemonic.address, transferAll=True, AsyncNum=1) #send all bnb | threadingNum, 
    
    #each transaction has a number, and if you send several transactions at once, one of them will not be sent, because it will have the same number as the previous one, by passing the number 
    # to this variable, you add some number to the current transaction: transferToken(), transferToken() = successful,error || transferToken(), transferToken(threadingNum=1) = successful,successful. 
    
    nonceTransferUsdt = await metaw3BSC.getNonce(address=addressWallet.address)
    transferUSDT = await metaw3BSC.transferToken(privateKey=newPrivateKey.privateKey, addressTo=newWalletWithMnemonic.address, contractAddressToken= '0x55d398326f99059ff775485246999027b3197955', qty=0.01, userNonce=nonceTransferUsdt.nonce)# send 0.01 usdt
    
    # userNonce, you can specify the transaction number yourself.
    
    transferUsdtAll = await metaw3BSC.transferToken(privateKey=newPrivateKey.privateKey, addressTo=newWalletWithMnemonic.address, contractAddressToken= '0x55d398326f99059ff775485246999027b3197955', transferAll=True, userNonce=nonceTransferUsdt.nonce+1)# send all usdt

    print(f"{newPrivateKey=}\n{newWalletWithMnemonic=}\n{addressWallet=}\n{balanceWallet=}\n{balanceWalletContractToken=}\n{nonce=}\n{transferBnb=}\n{transferBnbAll=}\n{transferUSDT=}\n{transferUsdtAll=}")

if __name__ == '__main__':
    run(testMetaWeb3())
```
![](https://cdn.discordapp.com/attachments/1041747038741745776/1041857018148966420/gif121.gif)

## **metaWeb3Async**
Function | Variables | #
:---: | --- | ---
*createWalletAsync* | **qty**:int|Create a new private key.
*getWalletAddressAsync* |**privateKeys**:list[str]|Gets the account address.
*createWalletWithMnemonicAsync* | **qty**:int|Create a new private key and mnemonic.
*getNonceAsync* |**addressList**:list[str]|Gets the transaction number 
*getBalanceWalletAsync* | **addressList**:list[str], **contractAddress**:str|Gets network token or contract token balance.


```python
from pyEasyWeb3 import metaWeb3Async
from asyncio import run

async def testMetaWeb3():
    metaw3BSC = metaWeb3Async() # network BSC

    newPrivateKey = await metaw3BSC.createWalletAsync(qty=10)

    newWalletWithMnemonic = await metaw3BSC.createWalletWithMnemonicAsync(qty=10)

    addressWallet = await metaw3BSC.getWalletAddressAsync(privateKeys=[key.privateKey for key in newPrivateKey])
    addressList = [address.address for address in addressWallet]

    balanceWallet = await metaw3BSC.getBalanceWalletAsync(addressList=addressList) # bnb 
    balanceWalletContractToken = await metaw3BSC.getBalanceWalletAsync(addressList=addressList, contractAddressToken='0x55d398326f99059ff775485246999027b3197955') # contract usdt (bsc network)

    nonce = await metaw3BSC.getNonceAsync(addressList=addressList)

    print(f"{newPrivateKey=}\n{newWalletWithMnemonic=}\n{addressWallet=}\n{balanceWallet=}\n{balanceWalletContractToken=}\n{nonce=}")

def syncDef():
    # ....
    privatKeys = run(metaWeb3Async().createWalletAsync(qty=10))
    for key in privatKeys:
        print(key.privateKey)

if __name__ == '__main__':
    run(testMetaWeb3())
    syncDef()
```
![](https://cdn.discordapp.com/attachments/1041747038741745776/1041787831745523724/2022-11-14-21-44-11-.gif)

## **exelData**
Function | Variables | #
:---: | --- | ---
*listNamedTupleToXlsx* | **data**:list[dataTypeClass], **fileName**:str|Creates an xlsx file.
*readXlsxFile* |**path**:str, **columnList**:list[str]|Reads columns in an xlsx file.

```python
from pyEasyWeb3 import metaWeb3Threading, exelData

def testMetaWeb3():
    metaw3BSC = metaWeb3Threading() # network BSC

    newWalletWithMnemonic = metaw3BSC.createWalletWithMnemonicThreading(qty=10)
    exelData.listNamedTupleToXlsx(data=newWalletWithMnemonic, fileName='test')
    read = exelData.readXlsxFile(path='test.xlsx', columnList=['a','b','c'])
    print(read)
    
if __name__ == '__main__':
    testMetaWeb3()
```
![](https://cdn.discordapp.com/attachments/1041747038741745776/1041863202759266324/2022-11-15-02-47-33-_online-video-cutter.com__1_.gif)
