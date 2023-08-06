#
from enum import Enum, auto


#


#


#
class BlockchainType(Enum):
    ETHEREUM = auto()
    BITCOIN = auto()


def blockchain_name(blockchain_name):
    available = {'ETHEREUM': BlockchainType.ETHEREUM,
                 'BITCOIN': BlockchainType.BITCOIN}
    if blockchain_name in available.keys():
        return available[blockchain_name]
    else:
        raise KeyError("Invalid blockchain type {0} is entered; please, check available ones".format(blockchain_type))


def blockchain_type(blockchain_type):
    available = {BlockchainType.ETHEREUM: 'ETHEREUM',
                 BlockchainType.BITCOIN: 'BITCOIN'}
    if blockchain_type in available.keys():
        return available[blockchain_type]
    else:
        raise KeyError("Invalid blockchain name {0} is entered; please, check available ones".format(blockchain_name))
