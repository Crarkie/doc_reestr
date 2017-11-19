from django.core.management.base import BaseCommand
from .models import Document
from .data.data_handler import DataHandler


def upload_document(address, passphrase, file_path):
    data_handler = DataHandler('localhost:5001', 'localhost:8545')

    print('Auth status: ', end='')
    print(data_handler.get_eth_provider().personal.unlockAccount(address, passphrase))
    print(address)
    print(passphrase)
    hash = data_handler.upload_document(file_path, address)['hash']

    state = data_handler.get_document(hash)['state']

    return { 'hash' : hash, 'state' : int(state.value) }