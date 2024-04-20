import json
import hashlib
import struct
from ripemd.ripemd160 import ripemd160  # import module
import ecdsa
from ecdsa import VerifyingKey, SECP256k1
from ecdsa.util import sigdecode_der

# takes a number and returns the variable integer in bytes
def int_to_varint(n):
    if n <= 252:  # 0xFC
        return n.to_bytes(1, 'little')
    elif n <= 65535:  # 0xFFFF
        return b'\xFD' + n.to_bytes(2, 'little')
    elif n <= 4294967295:  # 0xFFFFFFFF
        return b'\xFE' + n.to_bytes(4, 'little')
    else:
        return b'\xFF' + n.to_bytes(8, 'little')

# takes a string and returns the hash RIPEMD160(SHA256(string)) in hex
def OP_HASH160(string):
    bytes_string = bytes.fromhex(string)
    hash_sha256 = hashlib.sha256(bytes_string).digest()
    hash_ripemd160 = ripemd160(hash_sha256).hex()
    return hash_ripemd160

# takes a der encoded signature returns the r and s values in hex
'''
The Distinguished Encoding Rules (DER) format is used to encode ECDSA signatures in Bitcoin. An ECDSA signature is generated using a private key and a hash of the signed message. It consists of two 32-byte numbers (r,s). As described by Pieter here the DER signature format has the following components:

0x30 byte: header byte to indicate compound structure
one byte to encode the length of the following data
0x02: header byte indicating an integer
one byte to encode the length of the following r value
the r value as a big-endian integer
0x02: header byte indicating an integer
one byte to encode the length of the following s value
the s value as a big-endian integer


Note that the r and s value must be prepended with 0x00 if their first byte is greater than 0x80. This causes variable signature lengths in the case that the r value is in the upper half of the range (referred to as "high r"). Signatures with high s values are non-standard and usually don't appear in the wild. Also note that in rare cases r or s can be shorter than 32 bytes which is legal and leads to shorter signatures. Note that in bitcoin transactions a byte is added at the end of a DER signature denoting the SigHash type used.


'''
def get_r_s(signature):
    r_len = signature[6:8]
    r_len = int(r_len, 16) * 2
    r = signature[8:8 + r_len]
    if r_len>64 and r[0] == '0' and r[1] == '0':
        r = r[2:]
    s_len = signature[10+r_len:12+r_len]
    s_len = int(s_len, 16) * 2
    s = signature[12+r_len:12+r_len+s_len]
    if s_len>64 and s[0] == '0' and s[1] == '0':
        s = s[2:]
    # print(f'r: {r} and s: {s}')
    while((len(r))<64):
        r = '0' + r
    while((len(s))<64):
        s = '0' + s
    # print(r, s)
    return r, s


# takes a string(of hexa decimal) and returns their little endian
def hex_to_little_endian(hex_string):
    bytes_string = bytes.fromhex(hex_string)
    bytes_string = bytes_string[::-1]
    return bytes_string.hex()

'''
    This function returns the trimmed transaction for p2pkh verification.
    It follows the following steps:
    1. version: 4 bytes
    2. number of inputs: 1 byte
    3. for each input:
        if we are verifying the idx-th input and i == idx:
            - txid: 32 bytes
            - vout: 4 bytes
            - scriptSig length: 1 byte
            - scriptSig: variable
            - sequence: 4 bytes
        else:
            - txid: 32 bytes
            - vout: 4 bytes
            - scriptSig length: 0 byte
            - sequence: 4 bytes
    4. number of outputs: 1 byte
    5. for each output:
        - value: 8 bytes
        - scriptPubKey length: 1 byte
        - scriptPubKey: variable
    6. locktime: 4 bytes
    7. sighash_type: 4 bytes

    For better understanding, refer to the following link:
        https://github.com/LivioZ/P2PKH-Bitcoin-tx-verifier/blob/main/img/new_tx_dark.png
'''
def get_trimmed_transaction_p2pkh(version, locktime, vin, vout, idx):
    res = ''
    res += struct.pack('<I', version).hex()
    # len of vin in varint format
    res += int_to_varint(len(vin)).hex()
    for (i, input) in enumerate(vin):
        if i == idx:
            txid = hex_to_little_endian(input['txid'])
            res += txid
            res += struct.pack('<I', input['vout']).hex()
            res += struct.pack("<B", ((len(input['prevout']['scriptpubkey']))//2)).hex()
            # m = len(input['prevout']['scriptpubkey'])//2
            # res += int_to_varint(m).hex()
            res += bytes.fromhex(input['prevout']['scriptpubkey']).hex()
            res += struct.pack("<I", input['sequence']).hex()
        else:
            txid = hex_to_little_endian(input['txid'])
            res += txid
            res += struct.pack('<I', input['vout']).hex()
            res += struct.pack("<B", 0).hex()
            res += struct.pack("<I", input['sequence']).hex()
    res += int_to_varint(len(vout)).hex()
    for output in vout:
        res += struct.pack('<Q', output['value']).hex()
        res += struct.pack("<B", ((len(output['scriptpubkey']))//2)).hex()
        # res += int_to_varint((len(output['scriptpubkey'])//2)).hex()
        res += bytes.fromhex(output['scriptpubkey']).hex()
    res += struct.pack('<I', locktime).hex()
    sighash_type = "01000000" # SIGHASH_ALL
    res += sighash_type
    return res

def get_trimmed_transaction_p2sh(version, locktime, vin, vout, idx):
    message = ''
    message += struct.pack('<I', version).hex()
    message += int_to_varint(len(vin)).hex()
    for (i, input) in enumerate(vin):
        if i == idx:
            txid = hex_to_little_endian(input['txid'])
            message += txid
            message += struct.pack('<I', input['vout']).hex()
            # message += struct.pack("<B", ((len(input['scriptsig_asm'].split(' ')[-1]))//2)).hex()
            message += int_to_varint((len(input['scriptsig_asm'].split(' ')[-1])//2)).hex()
            message += bytes.fromhex(input['scriptsig_asm'].split(' ')[-1]).hex()
            message += struct.pack("<I", input['sequence']).hex()
        else:
            txid = hex_to_little_endian(input['txid'])
            message += txid
            message += struct.pack('<I', input['vout']).hex()
            message += struct.pack("<B", 0).hex()
            message += struct.pack("<I", input['sequence']).hex()
    # message += struct.pack('<B', len(vout)).hex()
    message += int_to_varint(len(vout)).hex()
    for output in vout:
        message += struct.pack('<Q', output['value']).hex()
        # message += struct.pack("<B", ((len(output['scriptpubkey']))//2)).hex()
        message += int_to_varint((len(output['scriptpubkey']))//2).hex()
        message += bytes.fromhex(output['scriptpubkey']).hex()
    message += struct.pack('<I', locktime).hex()
    message += "01000000"
    return message

# takes the signature in der format string, message in bytes and pubkey in hexa decimal string and returns True if the signature is valid using ECDSA
def OP_CHECKSIG(signature, pubkey, message):
    vk = VerifyingKey.from_string(bytes.fromhex(pubkey), curve=SECP256k1)
    r, s = get_r_s(signature)
    sig = r + s
    try:
        vk.verify(bytes.fromhex(sig),  message, hashlib.sha256)
        return True
    except:
        return False
    



def OP_CHECKMULTISIG(n, signatures, public_keys, message):
    for public_key in public_keys:
        for signature in signatures:
            if OP_CHECKSIG(signature, public_key, message):
                n -= 1
                signatures.remove(signature)
                public_keys.remove(public_key)
    
    if n > 0:
        return False
    return True

# takes message in hex and return double sha in hex
def DOUBLE_SHA256(message):
    message_bytes = bytes.fromhex(message)
    encoded_message = hashlib.sha256(hashlib.sha256(message_bytes).digest()).digest()
    return encoded_message.hex()


def hash256(message):
    message_bytes = bytes.fromhex(message)
    encoded_message = hashlib.sha256(hashlib.sha256(message_bytes).digest()).digest()
    return encoded_message.hex()


def merkle_parent_level(hashes):
    """takes a list of binary hashes and returns a list that's half of the length"""

    if len(hashes) % 2 == 1:
        hashes.append(hashes[-1])

    parent_level = []

    for i in range(0, len(hashes), 2):
        parent = hash256(hashes[i] + hashes[i + 1])
        parent_level.append(parent)
    return parent_level


def get_merkle_root(hashes):
    """Takes a list of binary hashes and return the merkle root"""
    current_level = hashes

    while len(current_level) > 1:
        current_level = merkle_parent_level(current_level)

    return current_level[0]


def serialise_transactions_for_wtxid(version, locktime, vin, vout):
    isSegwit = False
    res = ''
    witness = ''
    res += struct.pack('<I', version).hex()
    
    res += int_to_varint(len(vin)).hex()

    for input in vin:
        txid = hex_to_little_endian(input['txid'])
        res += txid
        res += struct.pack('<I', input['vout']).hex()
        res += struct.pack("<B", ((len(input['scriptsig']))//2)).hex()
        res += bytes.fromhex(input['scriptsig']).hex()
        res += struct.pack("<I", input['sequence']).hex()
        if input['prevout']['scriptpubkey_type'] == 'p2pkh' or input['prevout']['scriptpubkey_type'] == 'p2sh' or input['prevout']['scriptpubkey_type'] == '':
            # non-segwit
            witness += '00'
        else:
            # segwit
            isSegwit = True
            witness += struct.pack("<B", len(input['witness'])).hex()
            for w in input['witness']:
                witness += struct.pack("<B", ((len(w))//2)).hex()
                witness += bytes.fromhex(w).hex()

    res += int_to_varint(len(vout)).hex()

    for output in vout:
        res += struct.pack('<Q', output['value']).hex()
        res += struct.pack("<B", ((len(output['scriptpubkey']))//2)).hex()
        res += bytes.fromhex(output['scriptpubkey']).hex()

    if isSegwit:
        # insert marker and flag after version
        res = res[:8] + '0001' + res[8:]
        res += witness

    res += struct.pack('<I', locktime).hex()

    wtxid = DOUBLE_SHA256(res)
    return wtxid

def calc_txids(version, locktime, vin, vout):
    res = ''
    res += struct.pack('<I', version).hex()
    res += int_to_varint(len(vin)).hex()

    for input in vin:
        txid = hex_to_little_endian(input['txid'])
        res += txid
        res += struct.pack('<I', input['vout']).hex()
        res += struct.pack("<B", ((len(input['scriptsig']))//2)).hex()
        res += bytes.fromhex(input['scriptsig']).hex()
        res += struct.pack("<I", input['sequence']).hex()

    res += int_to_varint(len(vout)).hex()

    for output in vout:
        res += struct.pack('<Q', output['value']).hex()
        res += struct.pack("<B", ((len(output['scriptpubkey']))//2)).hex()
        res += bytes.fromhex(output['scriptpubkey']).hex()


    res += struct.pack('<I', locktime).hex()
    txid = DOUBLE_SHA256(res)
    # print(f'hello {txid}')
    return txid


def serialize_coinbase_transaction(version, locktime, vin, vout):
    res = ''
    res += struct.pack('<I', version).hex()

    # flag and marker
    res += '0001'

    res += int_to_varint(len(vin)).hex()

    for input in vin:
        res += hex_to_little_endian(input['txid'])
        res += struct.pack('<I', input['vout']).hex()
        res += struct.pack("<B", ((len(input['scriptsig']))//2)).hex()
        res += bytes.fromhex(input['scriptsig']).hex()
        res += struct.pack("<I", input['sequence']).hex()

    res += int_to_varint(len(vout)).hex()

    for output in vout:
        res += struct.pack('<Q', output['value']).hex()
        res += struct.pack("<B", ((len(output['scriptpubkey']))//2)).hex()
        res += bytes.fromhex(output['scriptpubkey']).hex()

    # witness for coinbase
    res += '01200000000000000000000000000000000000000000000000000000000000000000'

    res += struct.pack('<I', locktime).hex()

    return res