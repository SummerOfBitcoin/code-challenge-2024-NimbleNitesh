'''
Generate an output file named output.txt with the following structure:

First line: The block header.
Second line: The serialized coinbase transaction.
Following lines: The transaction IDs (txids) of the transactions mined in the block, in order. The first txid should be that of the coinbase transaction.
Difficulty Target:
The difficulty target is 0000ffff00000000000000000000000000000000000000000000000000000000. This is the value that the block hash must be less than for the block to be successfully mined.
'''

from transaction import Transaction
from utils import *
import struct
import time

def construct_coinbase_transaction(block_reward, transaction_fee, transactions):
    # create an empty coinbase transaction of type Transaction
    coinbase_transaction = Transaction('{"version":1,"locktime":0,"vin":[],"vout":[]}')
    coinbase_transaction.vin = [{
        "txid": "0000000000000000000000000000000000000000000000000000000000000000",
        "vout": 4294967295,
        "prevout": {
            "scriptpubkey": "",
            "scriptpubkey_asm": "",
            "scriptpubkey_type": "",
            "scriptpubkey_address": "",
            "value": 0
        },
        "scriptsig": "03233708184d696e656420627920416e74506f6f6c373946205b8160a4256c0000946e0100",
        "scriptsig_asm": "",
        "is_coinbase": True,
        "sequence": 0xFFFFFFFF,
        "witness": ["0000000000000000000000000000000000000000000000000000000000000000"]
    }]
    coinbase_transaction.vout = [{
        "value": block_reward + transaction_fee,
        "scriptpubkey": "41047eda6bd04fb27cab6e7c28c99b94977f073e912f25d1ff7165d9c95cd9bbe6da7e7ad7f2acb09e0ced91705f7616af53bee51a238b7dc527f2be0aa60469d140ac",
        "scriptpubkey_asm": "",
        "scriptpubkey_type": "",
        "scriptpubkey_address": "",
    }, 
    {
        "value": 0,
        "scriptpubkey": calculate_witness_commitment(transactions),
        "scriptpubkey_asm": "",
        "scriptpubkey_type": "",
        "scriptpubkey_address": "",
    }]
    return coinbase_transaction

def calculate_witness_commitment(transactions):
    # calculate the witness commitment
    wtxids = []
    wtxids.append('0000000000000000000000000000000000000000000000000000000000000000')
    for tx in transactions:
        wtxid = serialise_transactions_for_wtxid(tx.version, tx.locktime, tx.vin, tx.vout)
        wtxids.append(wtxid)

    # Should we sort? I am not sure.
    # wtxids.sort()

    # calculate the merkle root of the wtxids
    merkle_root = get_merkle_root(wtxids)
    merkle_root += '0000000000000000000000000000000000000000000000000000000000000000'

    witness_commitment = DOUBLE_SHA256(merkle_root)
    witness_commitment = '6a24aa21a9ed' + witness_commitment

    return witness_commitment


def construct_block(transactions, block_reward=6, transaction_fee=1):
    coinbase_transaction = construct_coinbase_transaction(block_reward, transaction_fee, transactions)
    transactions.insert(0, coinbase_transaction)
    block = assemble_blocks(transactions)
    difficulty_target = '0000ffff00000000000000000000000000000000000000000000000000000000'

    # mine the block
    mined_block = mine_blocks(block, difficulty_target)
    # print(mined_block)

    #generate block header
    block_header = serialise_block_header(block)

    first_transaction = mined_block['transactions'][0]
    # serialise coinbase transaction
    coinbase_tx = serialize_coinbase_transaction(first_transaction.version, first_transaction.locktime, first_transaction.vin, first_transaction.vout)
    txids = calc_txids_from_transactions(mined_block['transactions'])

    # write to output file block header, coinbase transaction and txids
    with open('../output.txt', 'w') as f:
        # write on a new line
        f.write(block_header + '\n')
        f.write(coinbase_tx + '\n')
        for txid in txids:
            txid = hex_to_little_endian(txid)
            f.write(txid + '\n')


def assemble_blocks(transactions):
    # assemble the block
    txids = calc_txids_from_transactions(transactions)
    merkle_root = get_merkle_root(txids)
    # print(txids)
    # print(merkle_root)
    block = {
        "version": '04000000',
        "prev_block": "0000000000000000000000000000000000000000000000000000000000000000",
        "merkle_root": merkle_root,
        # unix timestamp convert_to_4bytes(SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_secs() as u32)
        "timestamp": struct.pack('<I', int(time.time())).hex(),
        "bits": "ffff001f",
        "nonce": 0,
        "transactions": transactions
    }

    return block


'''

'''

def mine_blocks(block, difficulty_target):
    # mine the block
    block_header = block['version'] + block['prev_block'] + block['merkle_root'] + block['timestamp'] + block['bits']

    cur_nonce = 0
    while True:
        block_header_attemot = block_header + struct.pack('<I', cur_nonce).hex()
        # reverse in bytes format
        block_header_attemot = hex_to_little_endian(block_header_attemot)
        block_hash = DOUBLE_SHA256(block_header_attemot)
        # block hash in int and difficulty target in int and then compare
        if int(block_hash, 16) < int(difficulty_target, 16):
            break
        cur_nonce += 1

    block['nonce'] = cur_nonce
    return block

def serialise_block_header(block):
    # serialise the block header
    block_header = block['version'] + block['prev_block'] + block['merkle_root'] + block['timestamp'] + block['bits'] + struct.pack('<I', block['nonce']).hex()
    return block_header

def calc_txids_from_transactions(transactions):
    # calculate the txids from the transactions
    txids = []
    for tx in transactions:
        txid = calc_txids(tx.version, tx.locktime, tx.vin, tx.vout)
        txids.append(txid)
    return txids