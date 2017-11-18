# -*- coding: utf-8 -*-
# 2017, Kozlov Vasiliy <crarkie@gmail.com>

import logging
from .ipfs import IPFSProvider
from .ethereum import EthereumProvider
from .exceptions import *

class DataHandler:
    def __init__(self, ipfs_host, ethereum_host):
        ipfs_split = ipfs_host.split(':')
        ethereum_split = ethereum_host.split(':')

        if len(ipfs_split) != 2:
            raise ValueError('Incorrect IPFS host!')
        if len(ethereum_split) != 2:
            raise ValueError('Incorrect Ethereum host!')

        ipfs = { 'host' : ipfs_split[0], 'port' : ipfs_split[1] }
        ethereum = { 'host' : ethereum_split[0], 'port' : ethereum_split[1] }

        try:
            self.ipfs_provider = IPFSProvider(ipfs['host'], ipfs['port'])
            self.ethereum_provider = EthereumProvider(ethereum['host'], ethereum['port'])
        except (IPFSConnectionError, EthereumConnectionError) as connection_err:
            logging.error(str(connection_err))
            raise

