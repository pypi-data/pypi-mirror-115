# TODO: make these integers to save us some bytes
class BloxrouteMessageType:
    ABSTRACT_INTERNAL = None
    HELLO = b"hello"
    ACK = b"ack"
    PING = b"ping"
    PONG = b"pong"
    BROADCAST = b"broadcast"
    TRANSACTION = b"tx"
    GET_TRANSACTIONS = b"gettxs"
    TRANSACTIONS = b"txs"
    GET_TX_CONTENTS = b"getcontents"
    TX_CONTENTS = b"txcontents"
    KEY = b"key"
    BLOCK_HOLDING = b"blockhold"
    DISCONNECT_RELAY_PEER = b"droprelay"
    TX_SERVICE_SYNC_REQ = b"txstart"
    TX_SERVICE_SYNC_BLOCKS_SHORT_IDS = b"txblock"
    TX_SERVICE_SYNC_TXS = b"txtxs"
    TX_SERVICE_SYNC_COMPLETE = b"txdone"
    BLOCK_CONFIRMATION = b"blkcnfrm"
    TRANSACTION_CLEANUP = b"txclnup"
    NOTIFICATION = b"notify"
    BDN_PERFORMANCE_STATS = b"bdnstats"
    REFRESH_BLOCKCHAIN_NETWORK = b"blkntwrk"
    GET_COMPRESSED_BLOCK_TXS = b"getblocktxs"
    COMPRESSED_BLOCK_TXS = b"blocktxs"
    ROUTING_UPDATE = b"routing"
