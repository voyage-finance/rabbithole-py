import json
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract

# create web3 client connected to hardhat
w3 = Web3(HTTPProvider("http://localhost:8545"))
print("Connected? ", w3.isConnected())

# use the private key that was printed when running hardhat node
key="0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
# create a signer, for broadcasting transactions
eoa = w3.eth.account.privateKeyToAccount(key)

# load our bytecode and ABI.
artifact = json.load(open('./artifacts/contracts/Greeter.sol/Greeter.json'))
abi = artifact['abi'] # used to tell the client how to encode function parameters and so on
bytecode = artifact['bytecode'] # the compiled output of the contract, executed by the EVM
contract_factory = w3.eth.contract(bytecode=bytecode, abi=abi)

nonce = w3.eth.get_transaction_count(eoa.address)
tx_args = {
    'from': eoa.address,
    'nonce': nonce,
    'gas': 888888,
    'maxFeePerGas': w3.toWei('2', 'gwei'),
    'maxPriorityFeePerGas': w3.toWei('1', 'gwei')
}
tx = contract_factory.constructor(_name='ian').buildTransaction(tx_args)
signed_tx = eoa.signTransaction(tx)

# broadcast the transaction
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

# wait for confirmation
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("deployed at: ", tx_receipt['contractAddress'])

# call our contract
contract_instance = w3.eth.contract(abi=abi, address=tx_receipt['contractAddress'])
# we don't have to sign anything, since this is a `view` function and does not mutate world state
greeting = contract_instance.functions.greet().call()
print("greeting: ", greeting)

# we can set a new name, though.
nonce = w3.eth.get_transaction_count(eoa.address)
tx = contract_instance.functions.setName(_name="dake").buildTransaction({
    'from': eoa.address,
    'nonce': nonce,
    'gas': 888888,
    'maxFeePerGas': w3.toWei('2', 'gwei'),
    'maxPriorityFeePerGas': w3.toWei('1', 'gwei')
})
signed_tx = eoa.signTransaction(tx)
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
print("tx_hash: ", tx_hash)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("tx_receipt: ", tx_receipt)

greeting = contract_instance.functions.greet().call()
# "hello dake"
print("greeting: ", greeting)
