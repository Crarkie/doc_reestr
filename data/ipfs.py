# -*- coding: utf-8 -*-
# 2017, Kozlov Vasiliy <crarkie@gmail.com>

import ipfsapi
import ipfsapi.exceptions as ipfs_ex


class IPFSProvider:

    def __init__(self, host='localhost', port=5001):
        self.host = host
        self.port = port

        try:
            self.ipfs = ipfsapi.connect(host, port)
        except ipfs_ex.ConnectionError:
            raise IPFSConnectionError

    def upload_doc(self, doc_path) -> str:
        try:
            value = self.ipfs.add(doc_path)
        except ipfs_ex.StatusError:
            raise IPFSStatusError
        except ipfs_ex.ConnectionError:
            raise IPFSConnectionError

        return value['Hash']

    def download_doc(self, doc_hash):
        try:
            self.ipfs.get(doc_hash)
        except ipfs_ex.StatusError:
            raise IPFSStatusError
        except ipfs_ex.ConnectionError:
            raise IPFSConnectionError


class IPFSConnectionError(Exception):
    def __init__(self):
        self.msg = 'IPFS Connection error'
    def __str__(self):
        return self.msg


class IPFSStatusError(Exception):
    def __init__(self):
        self.msg = 'IPFS Status error'
    def __str__(self):
        return self.msg