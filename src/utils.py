import json
import hashlib
import struct
from ripemd.ripemd160 import ripemd160  # import module
from ecdsa import VerifyingKey, SECP256k1

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
            res += bytes.fromhex(input['prevout']['scriptpubkey']).hex()
            res += struct.pack("<I", input['sequence']).hex()
        else:
            txid = hex_to_little_endian(input['txid'])
            res += txid
            res += struct.pack('<I', input['vout']).hex()
            res += struct.pack("<B", 0).hex()
            res += struct.pack("<I", input['sequence']).hex()
    res += struct.pack('<B', len(vout)).hex()
    for output in vout:
        res += struct.pack('<Q', output['value']).hex()
        res += struct.pack("<B", ((len(output['scriptpubkey']))//2)).hex()
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
            message += struct.pack("<B", ((len(input['scriptsig_asm'].split(' ')[-1]))//2)).hex()
            message += bytes.fromhex(input['scriptsig_asm'].split(' ')[-1]).hex()
            message += struct.pack("<I", input['sequence']).hex()
        else:
            txid = hex_to_little_endian(input['txid'])
            message += txid
            message += struct.pack('<I', input['vout']).hex()
            message += struct.pack("<B", 0).hex()
            message += struct.pack("<I", input['sequence']).hex()
    message += struct.pack('<B', len(vout)).hex()
    for output in vout:
        message += struct.pack('<Q', output['value']).hex()
        message += struct.pack("<B", ((len(output['scriptpubkey']))//2)).hex()
        message += bytes.fromhex(output['scriptpubkey']).hex()
    message += struct.pack('<I', locktime).hex()
    message += "01000000"
    return message

# takes the signature in der format string, message in bytes and pubkey in hexa decimal string and returns True if the signature is valid using ECDSA
def OP_CHECKSIG(signature, pubkey, message):
    vk = VerifyingKey.from_string(bytes.fromhex(pubkey), curve=SECP256k1)
    r, s = get_r_s(signature)
    sig = r+s
    try:
        vk.verify(bytes.fromhex(sig),  message, hashlib.sha256)
        return True
    except:
        return False


