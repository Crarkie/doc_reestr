# -*- coding: utf-8 -*-
# 2017, Kozlov Vasiliy <crarkie@gmail.com>

import web3
import logging
import accounts as accs
from state import DocState
from time import sleep
from requests.exceptions import InvalidSchema


class EthereumProvider:
    def __init__(self, host='localhost', port='8545'):
        try:
            self.ethereum = web3.Web3(web3.HTTPProvider('{host}:{port}'.format(host=host, port=port)))
            self.ethereum.eth.blockNumber
            self.contract = None
        except InvalidSchema:
            logging.error('Cannot connect to ethereum provider!')
            raise EthereumConnectionError

    def deploy_contract(self, address=None):
        self.contract = EthereumContract(self.ethereum, address)
        return self.contract.get_contract_address()

    def get_provider(self):
        return self.ethereum

    def get_contract(self):
        return self.contract


class EthereumContract:
    def __init__(self, provider, address=None):
        self.gasPrice = web3.Web3.toWei(20, 'gwei')
        self.provider = provider
        code = '6060604052336000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550610986806100536000396000f300606060405260043610610083576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff1680632ec2c246146100885780632fbac059146100c15780634420e486146100e85780636fca1744146101215780638da5cb5b1461019d5780638e5ed2bd146101f2578063f2fde38b14610219575b600080fd5b341561009357600080fd5b6100bf600480803573ffffffffffffffffffffffffffffffffffffffff16906020019091905050610252565b005b34156100cc57600080fd5b6100e660048080356000191690602001909190505061032e565b005b34156100f357600080fd5b61011f600480803573ffffffffffffffffffffffffffffffffffffffff16906020019091905050610511565b005b341561012c57600080fd5b6101466004808035600019169060200190919050506105ed565b604051808373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200182600281111561018857fe5b60ff1681526020019250505060405180910390f35b34156101a857600080fd5b6101b061063e565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b34156101fd57600080fd5b610217600480803560001916906020019091905050610663565b005b341561022457600080fd5b610250600480803573ffffffffffffffffffffffffffffffffffffffff16906020019091905050610805565b005b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff161415156102ad57600080fd5b60008173ffffffffffffffffffffffffffffffffffffffff16141515156102d357600080fd5b6000600260008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548160ff02191690831515021790555050565b600260003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900460ff16151561038657600080fd5b6000600281111561039357fe5b60016000836000191660001916815260200190815260200160002060000160149054906101000a900460ff1660028111156103ca57fe5b1415156103d657600080fd5b60408051908101604052803373ffffffffffffffffffffffffffffffffffffffff1681526020016001600281111561040a57fe5b81525060016000836000191660001916815260200190815260200160002060008201518160000160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555060208201518160000160146101000a81548160ff0219169083600281111561049357fe5b02179055509050507f12a84e570dee4b071bef44278d8d547f7fbd93e8fe27e954afd9b798e3a6438f3382604051808373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200182600019166000191681526020019250505060405180910390a150565b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff1614151561056c57600080fd5b60008173ffffffffffffffffffffffffffffffffffffffff161415151561059257600080fd5b6001600260008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548160ff02191690831515021790555050565b60016020528060005260406000206000915090508060000160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16908060000160149054906101000a900460ff16905082565b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b600260003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900460ff1615156106bb57600080fd5b600160028111156106c857fe5b60016000836000191660001916815260200190815260200160002060000160149054906101000a900460ff1660028111156106ff57fe5b14151561070b57600080fd5b60016000826000191660001916815260200190815260200160002060000160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff1614151561078357600080fd5b600260016000836000191660001916815260200190815260200160002060000160146101000a81548160ff021916908360028111156107be57fe5b02179055507f3e01a6e8a8aff0ecfda754c31ace3d6e6931b63c96478a098b093b22b081e3e48160405180826000191660001916815260200191505060405180910390a150565b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff1614151561086057600080fd5b600073ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff161415151561089c57600080fd5b8073ffffffffffffffffffffffffffffffffffffffff166000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff167f8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e060405160405180910390a3806000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550505600a165627a7a723058203bca4c5fcad93be7c88716f867b2fa99511a9734925354133b168a9a90aae33b0029'
        code_runtime = '606060405260043610610083576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff1680632ec2c246146100885780632fbac059146100c15780634420e486146100e85780636fca1744146101215780638da5cb5b1461019d5780638e5ed2bd146101f2578063f2fde38b14610219575b600080fd5b341561009357600080fd5b6100bf600480803573ffffffffffffffffffffffffffffffffffffffff16906020019091905050610252565b005b34156100cc57600080fd5b6100e660048080356000191690602001909190505061032e565b005b34156100f357600080fd5b61011f600480803573ffffffffffffffffffffffffffffffffffffffff16906020019091905050610511565b005b341561012c57600080fd5b6101466004808035600019169060200190919050506105ed565b604051808373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200182600281111561018857fe5b60ff1681526020019250505060405180910390f35b34156101a857600080fd5b6101b061063e565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b34156101fd57600080fd5b610217600480803560001916906020019091905050610663565b005b341561022457600080fd5b610250600480803573ffffffffffffffffffffffffffffffffffffffff16906020019091905050610805565b005b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff161415156102ad57600080fd5b60008173ffffffffffffffffffffffffffffffffffffffff16141515156102d357600080fd5b6000600260008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548160ff02191690831515021790555050565b600260003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900460ff16151561038657600080fd5b6000600281111561039357fe5b60016000836000191660001916815260200190815260200160002060000160149054906101000a900460ff1660028111156103ca57fe5b1415156103d657600080fd5b60408051908101604052803373ffffffffffffffffffffffffffffffffffffffff1681526020016001600281111561040a57fe5b81525060016000836000191660001916815260200190815260200160002060008201518160000160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555060208201518160000160146101000a81548160ff0219169083600281111561049357fe5b02179055509050507f12a84e570dee4b071bef44278d8d547f7fbd93e8fe27e954afd9b798e3a6438f3382604051808373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200182600019166000191681526020019250505060405180910390a150565b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff1614151561056c57600080fd5b60008173ffffffffffffffffffffffffffffffffffffffff161415151561059257600080fd5b6001600260008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548160ff02191690831515021790555050565b60016020528060005260406000206000915090508060000160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16908060000160149054906101000a900460ff16905082565b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b600260003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900460ff1615156106bb57600080fd5b600160028111156106c857fe5b60016000836000191660001916815260200190815260200160002060000160149054906101000a900460ff1660028111156106ff57fe5b14151561070b57600080fd5b60016000826000191660001916815260200190815260200160002060000160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff1614151561078357600080fd5b600260016000836000191660001916815260200190815260200160002060000160146101000a81548160ff021916908360028111156107be57fe5b02179055507f3e01a6e8a8aff0ecfda754c31ace3d6e6931b63c96478a098b093b22b081e3e48160405180826000191660001916815260200191505060405180910390a150565b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff1614151561086057600080fd5b600073ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff161415151561089c57600080fd5b8073ffffffffffffffffffffffffffffffffffffffff166000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff167f8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e060405160405180910390a3806000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550505600a165627a7a723058203bca4c5fcad93be7c88716f867b2fa99511a9734925354133b168a9a90aae33b0029'
        abi = [{"constant":False,"inputs":[{"name":"user","type":"address"}],"name":"unregister","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"name":"hash","type":"bytes32"}],"name":"createDoc","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"name":"user","type":"address"}],"name":"register","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"name":"","type":"bytes32"}],"name":"docs","outputs":[{"name":"creator","type":"address"},{"name":"state","type":"uint8"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"hash","type":"bytes32"}],"name":"outdateDoc","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"anonymous":False,"inputs":[{"indexed":False,"name":"creator","type":"address"},{"indexed":False,"name":"hash","type":"bytes32"}],"name":"DocCreated","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"name":"hash","type":"bytes32"}],"name":"DocOutdated","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"name":"previousOwner","type":"address"},{"indexed":True,"name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"}]


        if address:
            self.contract = provider.eth.contract(address=address, abi=abi)
        else:
            self.contract = provider.eth.contract(abi=abi, bytecode=code, bytecode_runtime=code_runtime)
            self.provider.personal.unlockAccount(accs.registerAddress, accs.registerPassphrase)
            tx_hash = self.contract.deploy({'from': accs.registerAddress, 'gasPrice':self.gasPrice, 'gas':1000000})

            print('TX: {0}'.format(tx_hash))
            transaction = self.pending_transaction(tx_hash)
            self.contract.address = transaction['contractAddress']

            logging.info('Deploy contract, TX: {tx}, ADDR: {addr}'.format(tx=tx_hash, addr=self.contract.address))

    def pending_transaction(self, tx):
        transaction = self.provider.eth.getTransactionReceipt(tx)
        while transaction is None or transaction['blockNumber'] is None:
            sleep(1)
            transaction = self.provider.eth.getTransactionReceipt(tx)
        print('Transaction gas used: {gas}'.format(gas=transaction['gasUsed']))
        return transaction

    def get_contract_address(self):
        return self.contract.address

    def register_user(self, address):
        self.provider.personal.unlockAccount(accs.registerAddress, accs.registerPassphrase)
        tx_hash = self.contract.transact({'from':accs.registerAddress, 'gasPrice':self.gasPrice}).register(address)
        self.pending_transaction(tx_hash)

    def unregister_user(self, address):
        self.provider.personal.unlockAccount(accs.registerAddress, accs.registerPassphrase)
        tx_hash = self.contract.transact({'from':accs.registerAddress, 'gasPrice':self.gasPrice}).unregister(address)
        self.pending_transaction(tx_hash)

    def get_document(self, hash):
        self.provider.personal.unlockAccount(accs.registerAddress, accs.registerPassphrase)
        doc = self.contract.call({'from':accs.registerAddress}).docs(hash)
        return { 'creator' : doc[0], 'state' : DocState(doc[1]) }

    def create_document(self, hash, address):
        tx_hash = self.contract.transact({'from':address, 'gasPrice':self.gasPrice, 'gas':60000}).createDoc(hash)
        self.pending_transaction(tx_hash)

        return { 'status' : self.get_document(hash)['state'] }

    def outdate_document(self, hash, address):
        tx_hash = self.contract.transact({'from':address, 'gasPrice':self.gasPrice, 'gas':60000}).outdateDoc(hash)
        self.pending_transaction(tx_hash)

        return { 'status' : self.get_document(hash)['state'] }


class EthereumConnectionError(Exception):
    def __init__(self):
        self.msg = 'Ethereum Connection error'
    def __str__(self):
        return self.msg