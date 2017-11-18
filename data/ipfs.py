# -*- coding: utf-8 -*-
# 2017, Kozlov Vasiliy <crarkie@gmail.com>

import ipfsapi


class IPFSProvider:

    def __init__(self, host='localhost', port=5001):
        self.host = host
        self.port = port

        self.ipfs = ipfsapi.connect(host, port)

    def upload_doc(self, doc_path) -> str:
        value = self.ipfs.add(doc_path)

        return value['Hash']

    def download_doc(self, doc_hash):
        self.ipfs.get(doc_hash)


class IPFSConnectionError(Exception):
    def __init__(self):
        self.msg = 'IPFS Connection error'
    def __str__(self):
        return self.msg