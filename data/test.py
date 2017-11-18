#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from data_handler import DataHandler

test_user = '0x51d52be22399dce37232f85001d0a4031d63d6f6'

def main():
    handler = DataHandler('localhost:5001', '46.191.178.77:54845')

    print('Contract address: {0}'.format(handler.ethereum_provider.get_contract().get_contract_address()))

    handler.register_account(test_user)
    provider = handler.get_eth_provider()

    provider.personal.unlockAccount(test_user, 'hhh555r4o9')
    doc = handler.upload_document('test.pdf', test_user)

    print('Doc status: {st}\nHash: {hash}'.format(st=doc['status'], hash=doc['hash']))
    print('Try get doc from blockchain...')

    hash = doc['hash']
    doc = handler.get_document(doc['hash'])

    print('Doc status: {st}\nCreator: {cr}'.format(st=doc['state'], cr=doc['creator']))
    print('Try to outdate doc...')

    provider.personal.unlockAccount(test_user, 'hhh555r4o9')
    doc = handler.outdate_document(test_user, hash)

    doc = handler.get_document(hash)

    print('Doc status: {st}\nCreator: {cr}'.format(st=doc['state'], cr=doc['creator']))

    handler.save_contract()

if __name__ == '__main__':
    main()