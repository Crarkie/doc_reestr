#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from data_handler import DataHandler
from base58 import b58encode
from state import DocState

test_user = '0x2abdfd2bb95d2c98986e21e76c1f9e8179c84c8a'

def main():
    handler = DataHandler('localhost:5001', 'localhost:8545')

    print('Contract address: {0}'.format(handler.ethereum_provider.get_contract().get_contract_address()))
    #handler.save_contract()

    handler.register_account(test_user)
    provider = handler.get_eth_provider()

    provider.personal.unlockAccount(test_user, 'hhh555r4o9')
    doc = handler.upload_document('accounts.py', test_user)

    print('Doc hash: {hash}'.format(hash=b58encode(doc['hash'])))
    print('Try get doc from blockchain...')

    hash = doc['hash']
    doc = handler.get_document(hash)

    print('Doc status: {st}\nCreator: {cr}'.format(st=doc['state'], cr=doc['creator']))
    print('Try to outdate doc...')


    provider.personal.unlockAccount(test_user, 'hhh555r4o9')
    doc = handler.outdate_document(hash, test_user)
    doc = handler.get_document(hash)
    print('Doc status: {st}\nCreator: {cr}'.format(st=doc['state'], cr=doc['creator']))
    handler.unregister_account(test_user)
    exit(0)

if __name__ == '__main__':
    main()