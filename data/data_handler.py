# -*- coding: utf-8 -*-
# 2017, Kozlov Vasiliy <crarkie@gmail.com>

import logging
import web3
import json
from ipfs import IPFSProvider
from ethereum import EthereumProvider
from exceptions import *
from enum import Enum

class DocState(Enum):
    Empty = 0,
    Active = 1,
    Outdated = 2

class DataHandler:
    def __init__(self, ipfs_host, ethereum_host, contract_file='contract_address.json'):
        ipfs_split = ipfs_host.split(':')
        ethereum_split = ethereum_host.split(':')
        self.contract_file = contract_file

        address = None
        try:
            with open(contract_file, 'r') as cfile:
                address = json.load(cfile).get('contract_address', None)
        except OSError:
            logging.error('Cannot open contract config file!')
            exit(-1)

        if len(ipfs_split) != 2:
            raise ValueError('Incorrect IPFS host!')
        if len(ethereum_split) != 2:
            raise ValueError('Incorrect Ethereum host!')

        ipfs = { 'host' : ipfs_split[0], 'port' : ipfs_split[1] }
        ethereum = { 'host' : ethereum_split[0], 'port' : ethereum_split[1] }

        try:
            self.ipfs_provider = IPFSProvider(ipfs['host'], ipfs['port'])
            self.ethereum_provider = EthereumProvider('http://{0}'.format(ethereum['host']), ethereum['port'])
        except (IPFSConnectionError, EthereumConnectionError) as connection_err:
            logging.error(str(connection_err))
            raise
        self.ethereum_provider.deploy_contract(address)

    def save_contract(self):
        with open(self.contract_file, 'w') as cfile:
            json.dump({'contract_address':self.ethereum_provider.get_contract().get_contract_address()}, cfile, indent=4)

    def upload_document(self, doc_path, address):
        file_hash = self.ipfs_provider.upload_doc(doc_path)
        transaction = self.ethereum_provider.get_contract().create_document(file_hash, address)

        return { 'status' : transaction['status'], 'hash' : file_hash }

    def outdate_document(self, hash, address):
        transaction = self.ethereum_provider.get_contract().outdate_document(hash, address)

        return { 'status' : transaction['status']}

    def get_document(self, hash):
        doc = self.ethereum_provider.get_contract().get_document(hash)

        if doc['state'] == DocState.Empty:
            return {'state': DocState.Empty, 'creator' : ''}
        else:
            self.ipfs_provider.download_doc(hash)
            return {'state': doc['state'], 'creator' : doc['creator']}

    def register_account(self, address):
        self.ethereum_provider.get_contract().register_user(address)

    def unregister_account(self, address):
        self.ethereum_provider.get_contract().unregister_user(address)

    def get_eth_provider(self):
        return self.ethereum_provider.get_provider()



