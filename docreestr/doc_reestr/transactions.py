from django.core.management.base import BaseCommand
from data.data_handler import DataHandler
from .models import Document

class UploadCommand(BaseCommand):
    help = 'Upload file to blockchain and IPFS'

    def add_arguments(self, parser):
        parser.add_argument('doc_id', nargs=1, type=int, required=True)
        parser.add_argument('file_path', nargs=1, type=str, required=True)
        parser.add_argument('address', nargs=1, type=str, required=True)
        parser.add_argument('passphrase', nargs=1, type=str, required=True)

    def handle(self, *args, **opts):
        data_handler = DataHandler('localhost:5001', 'localhost:8545')

        data_handler.get_eth_provider().personal.unlockAccount(opts['address'][0], opts['passphrase'][0])
        hash = data_handler.upload_document(opts['file_path'][0], opts['address'][0])['hash']
        doc = data_handler.get_document(hash)

        document = Document.objects.get(id=opts['doc_id'][0])
        document.hash_file = hash
        document.id_status = int(doc['state'])
        document.save()