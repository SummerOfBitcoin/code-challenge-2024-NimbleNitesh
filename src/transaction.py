import json
import hashlib
import struct
from ripemd.ripemd160 import ripemd160  # import module
import ecdsa
from ecdsa import VerifyingKey, SECP256k1
from ecdsa.util import sigdecode_der


# File: 0a8b21af1cfcc26774df1f513a72cd362a14f5a598ec39d915323078efb5a240
# File: 2fd01ea275a839414d6f594ad9355734915a2c71c3da5baaff42b38ed564c0d0


data = {
  "version": 1,
  "locktime": 0,
  "vin": [
    {
      "is_coinbase": False,
      "txid": "a1075db55d416d3ca199f55b6084e2115b9345e16c5cf302fc80e9d5fbf5d48d",
      "vout": 0,
      "scriptsig": "4830450221009908144ca6539e09512b9295c8a27050d478fbb96f8addbc3d075544dc41328702201aa528be2b907d316d2da068dd9eb1e23243d97e444d59290d2fddf25269ee0e0141042e930f39ba62c6534ee98ed20ca98959d34aa9e057cda01cfd422c6bab3667b76426529382c23f42b9b08d7832d4fee1d6b437a8526e59667ce9c4e9dcebcabb",
      "scriptsig_asm": "OP_PUSHBYTES_72 30450221009908144ca6539e09512b9295c8a27050d478fbb96f8addbc3d075544dc41328702201aa528be2b907d316d2da068dd9eb1e23243d97e444d59290d2fddf25269ee0e01 OP_PUSHBYTES_65 042e930f39ba62c6534ee98ed20ca98959d34aa9e057cda01cfd422c6bab3667b76426529382c23f42b9b08d7832d4fee1d6b437a8526e59667ce9c4e9dcebcabb",
      "sequence": 4294967295,
      "prevout": {
        "scriptpubkey": "76a91446af3fb481837fadbb421727f9959c2d32a3682988ac",
        "scriptpubkey_asm": "OP_DUP OP_HASH160 OP_PUSHBYTES_20 46af3fb481837fadbb421727f9959c2d32a36829 OP_EQUALVERIFY OP_CHECKSIG",
        "value": 1000000000000,
        "scriptpubkey_address": "17SkEw2md5avVNyYgj6RiXuQKNwkXaxFyQ",
        "scriptpubkey_type": "p2pkh"
      }
    }
  ],
  "vout": [
    {
      "scriptpubkey_address": "1MLh2UVHgonJY4ZtsakoXtkcXDJ2EPU6RY",
      "scriptpubkey": "76a914df1bd49a6c9e34dfa8631f2c54cf39986027501b88ac",
      "scriptpubkey_type": "p2pkh",
      "value": 577700000000
    },
    {
      "scriptpubkey_address": "13TETb2WMr58mexBaNq1jmXV1J7Abk2tE2",
      "scriptpubkey": "4104cd5e9726e6afeae357b1806be25a4c3d3811775835d235417ea746b7db9eeab33cf01674b944c64561ce3388fa1abd0fa88b06c44ce81e2234aa70fe578d455dac",
      "scriptpubkey_type": "p2pk",
      "value": 422300000000
    }
  ]
}

def hex_to_little_endian(hex_string):
    # print(hex_string)
    bytes_string = bytes.fromhex(hex_string)
    bytes_string = bytes_string[::-1]
    # print(bytes_string.hex())
    # print("hello")
    return bytes_string.hex()

class Transaction:
    def __init__(self, json_data):
        data_dict = json.loads(json_data)  # Convert JSON string to dictionary
        self.version = data_dict.get("version")
        self.locktime = data_dict.get("locktime")
        self.vin = data_dict.get("vin")
        self.vout = data_dict.get("vout")

    def get_r_s(self, signature):
        r_len = signature[6:8]
        r_len = int(r_len, 16) * 2
        self.r = signature[8:8 + r_len]
        if self.r[0] == '0' and self.r[1] == '0':
            self.r = self.r[2:]
        s_len = signature[10+r_len:12+r_len]
        s_len = int(s_len, 16) * 2
        self.s = signature[12+r_len:12+r_len+s_len]
        if self.s[0] == '0' and self.s[1] == '0':
            self.s = self.s[2:]

    
    def get_raw_transaction(self):
        self.raw_transaction = ''
        self.raw_transaction += struct.pack("<I", self.version).hex()
        self.raw_transaction += struct.pack("<B", len(self.vin)).hex()
        for input in self.vin:
            # transaction id should go in little ednian format. 4a03 should be 034a
            txid = hex_to_little_endian(input['txid'])
            self.raw_transaction += txid
            # self.raw_transaction += bytes.fromhex(input['txid']).hex()
            self.raw_transaction += struct.pack("<I", input['vout']).hex()
            self.raw_transaction += struct.pack("<B", ((len(input['scriptsig']))//2)).hex()
            self.raw_transaction += bytes.fromhex(input['scriptsig']).hex()
            self.raw_transaction += struct.pack("<I", input['sequence']).hex()
        self.raw_transaction += struct.pack("<B", len(self.vout)).hex()
        for output in self.vout:
            self.raw_transaction += struct.pack("<Q", output['value']).hex()
            self.raw_transaction += struct.pack("<B", ((len(output['scriptpubkey'])//2))).hex()
            self.raw_transaction += bytes.fromhex(output['scriptpubkey']).hex()
        self.raw_transaction += struct.pack("<I", self.locktime).hex()
        # print(f'Raw Transaction is {self.raw_transaction}')

    def trimmed_txn(self):
        self.trimmed_tx = ''
        self.trimmed_tx += struct.pack("<I", self.version).hex()
        self.trimmed_tx += struct.pack("<B", len(self.vin)).hex()
        for input in self.vin:
            txid = hex_to_little_endian(input['txid'])
            self.trimmed_tx += txid
            # self.trimmed_tx += bytes.fromhex(input['txid']).hex()
            self.trimmed_tx += struct.pack("<I", input['vout']).hex()
            self.trimmed_tx += struct.pack("<B", ((len(input['prevout']['scriptpubkey']))//2)).hex()
            self.trimmed_tx += bytes.fromhex(input['prevout']['scriptpubkey']).hex()
            self.trimmed_tx += struct.pack("<I", input['sequence']).hex()
        self.trimmed_tx += struct.pack("<B", len(self.vout)).hex()
        for output in self.vout:
            self.trimmed_tx += struct.pack("<Q", output['value']).hex()
            self.trimmed_tx += struct.pack("<B", ((len(output['scriptpubkey']))//2)).hex()
            self.trimmed_tx += bytes.fromhex(output['scriptpubkey']).hex()
        self.trimmed_tx += struct.pack("<I", self.locktime).hex()
        sighash_type = "01000000"  # SIGHASH_ALL
        self.trimmed_tx += sighash_type
        # print(f'Trimmed Transaction is {self.trimmed_tx}')

    def validate(self):
        # Validate the transaction
        for input in self.vin:
            # print(input['prevout']['scriptpubkey_type'])
            try:
                if input['prevout']['scriptpubkey_type'] == "p2pkh":
                    scriptsig_asm = input['scriptsig_asm'].split(' ')[-1]
                    #covert to binary
                    scriptsig_asm = bytes.fromhex(scriptsig_asm)

                    # hash SHA256
                    hash_sha256 = hashlib.sha256(scriptsig_asm).digest()
                    # hash RIPEMD160
                    hash_ripemd160 = ripemd160(hash_sha256).hex()
                    # print(hash_ripemd160)
                    # Check if the hash is equal to the address
                    scriptpubkey_asm = input['prevout']['scriptpubkey_asm']
                    # split by ' ' and then find the 3 word
                    address = scriptpubkey_asm.split(' ')[3]
                    # if address == hash_ripemd160:
                    # print(address, hash_ripemd160)
                    # print(address, hash_ripemd160)
                    assert(len(address) == len(hash_ripemd160))
                    if address != hash_ripemd160:
                        print('Invalid transaction')
                        return
                    signature = input['scriptsig_asm'].split(' ')[1]
                    # print(signature)
                    self.get_r_s(signature)
                    self.get_raw_transaction()
                    self.trimmed_txn()

                    message = bytes.fromhex(self.trimmed_tx)
                    message = hashlib.sha256(message).digest()
                    # print(f'Message is {message.hex()}')

                    signature = self.r + self.s

                    public_key = input['scriptsig_asm'].split(' ')[-1]

                    vk = VerifyingKey.from_string(bytes.fromhex(public_key), curve=SECP256k1)
                    vk.verify(bytes.fromhex(signature), message, hashlib.sha256)
                    return True
                else:
                    # print('Work in progress')
                    return False

            except Exception as e:
                # print('Invalid transaction')
                return False
            
        for output in self.vout:
            if output['scriptpubkey_type'] == "p2pkh":
                pass
            else:
                pass
        


# obj = Transaction(json.dumps(data))
# obj.validate()
# obj.get_raw_transaction()



'''
        It is composed by:

version: 4 bytes
01 00 00 00
input count: 1 bytes
01
Inputs section:

previous tx id (little endian form): 32 bytes
90df970d7f7f2881258da9dbf6205f85839a2eb8ec88298e5db313fc2a239377
previous output index: 4 bytes
00 00 00 00
script (composed by <sig> <pubkey>) length: 1 byte
6b (which is 107 bytes)
<sig> length: 1 byte
48 (which is 72 bytes)
DER signature marker: 1 byte
30
signature length: 1 byte
45 (which is 69 bytes)
r value marker: 1 byte
02
r value length: 1 byte
21 (which is 33 bytes)
r value: 33 bytes
00e384d96b1b12df38f3f8fcf606e4b7a4e2f5f65c6b724af26291bd0de188191b
s value marker: 1 byte
02
s value length: 1 byte
20 (which is 32 bytes)
s value: 32 bytes
249fac61c20f564ac89f06fe7502270820e694299d0d2e28dcc188089901eb9c
The signature is R + S without 00 in R

e384d96b1b12df38f3f8fcf606e4b7a4e2f5f65c6b724af26291bd0de188191b249fac61c20f564ac89f06fe7502270820e694299d0d2e28dcc188089901eb9c
sighash flag, if = 01 then the signature applies to all the inputs and the outputs, this is the most common for P2PKH transactions
01
<pubKey> length: 1 byte
21 (which is 33 bytes)
The public key is:

0369e03e2c91f0badec46c9c903d9e9edae67c167b9ef9b550356ee791c9a40896
sequence number: 4 bytes
ffffffff (which is the default value)
Outputs section:

output count: 1 byte
02
number of satoshis to spend (output #1): 8 bytes
a1a2960200000000
pubkey script length (output #1): 1 byte
19(which is 25 bytes)
pubkey script (output #1): 25 bytes
76a9149f21a07a0c7c3cf65a51f586051395762267cdaf88ac
number of satoshis to spend (output #2): 8 bytes
a09e390000000000
pubkey script length (output #2): 1 byte
19(which is 25 bytes)
pubkey script (output #2): 25 bytes
76a91402f9d6bafab13b2bbd68d1dc380f3f8bbddc3dc388ac
unix epoch time or block number: 4 bytes
00000000



actual raw: 01000000019c2e0f24a03e72002a96acedb12a632e72b6b74c05dc3ceab1fe78237f886c48010000006a47304402203da9d487be5302a6d69e02a861acff1da472885e43d7528ed9b1b537a8e2cac9022002d1bca03a1e9715a99971bafe3b1852b7a4f0168281cbd27a220380a01b3307012102c9950c622494c2e9ff5a003e33b690fe4832477d32c2d256c67eab8bf613b34effffffff02b6f50500000000001976a914bdf63990d6dc33d705b756e13dd135466c06b3b588ac845e0201000000001976a9145fb0e9755a3424efd2ba0587d20b1e98ee29814a88ac00000000

code raw: 0100000001486c887f2378feb1ea3cdc054cb7b6722e632ab1edac962a00723ea0240f2e9c010000006a47304402203da9d487be5302a6d69e02a861acff1da472885e43d7528ed9b1b537a8e2cac9022002d1bca03a1e9715a99971bafe3b1852b7a4f0168281cbd27a220380a01b3307012102c9950c622494c2e9ff5a003e33b690fe4832477d32c2d256c67eab8bf613b34effffffff02b6f50500000000001976a914bdf63990d6dc33d705b756e13dd135466c06b3b588ac845e0201000000001976a9145fb0e9755a3424efd2ba0587d20b1e98ee29814a88ac00000000
        '''