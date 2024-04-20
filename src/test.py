from utils import *
import struct

data = {
  "version": 2,
  "locktime": 0,
  "vin": [
    {
      "txid": "92fbab1c8c0333fa5d0dec7a0dcb075f120659acafdcc3ed34382d08564ef427",
      "vout": 1,
      "prevout": {
        "scriptpubkey": "00142d11e19fc68c504f600d4837cd6cff9d15dab700",
        "scriptpubkey_asm": "OP_0 OP_PUSHBYTES_20 2d11e19fc68c504f600d4837cd6cff9d15dab700",
        "scriptpubkey_type": "v0_p2wpkh",
        "scriptpubkey_address": "bc1q95g7r87x33gy7cqdfqmu6m8ln52a4dcq2cdg73",
        "value": 2084318
      },
      "scriptsig": "",
      "scriptsig_asm": "",
      "witness": [
        "3045022100a792f9eb754d0276829485da86cab4415d8b3ba415230747d545fb514420c2a3022043cb39eccd56b047c2a41b26de36ae8fdd4028c7f3f003d15e16ad5df16b791e01",
        "0300af51fb8f6ecb4a3a26b5d0b542e9ec0a660581c6e65c820184bfb052d3422b"
      ],
      "is_coinbase": False,
      "sequence": 2147483648
    }
  ],
  "vout": [
    {
      "scriptpubkey": "00141ee1bf613d84297673702590b1176c1e8ac9a54d",
      "scriptpubkey_asm": "OP_0 OP_PUSHBYTES_20 1ee1bf613d84297673702590b1176c1e8ac9a54d",
      "scriptpubkey_type": "v0_p2wpkh",
      "scriptpubkey_address": "bc1qrmsm7cfass5hvumsykgtz9mvr69vnf2d5y6fpn",
      "value": 1065936
    },
    {
      "scriptpubkey": "00142df81a0545b44f39af421c551255157ba4efa3c4",
      "scriptpubkey_asm": "OP_0 OP_PUSHBYTES_20 2df81a0545b44f39af421c551255157ba4efa3c4",
      "scriptpubkey_type": "v0_p2wpkh",
      "scriptpubkey_address": "bc1q9hup5p29k38nnt6zr323y4g40wjwlg7yg2p7tj",
      "value": 1014002
    }
  ]
}

from utils import *


def serialize(version, locktime, vin, vout, idx):
    res = ''
    res += struct.pack('<I', version).hex()
    hashPrevouts = ''
    for input in vin:
        hashPrevouts += hex_to_little_endian(input['txid'])
        hashPrevouts += struct.pack('<I', input['vout']).hex()
    res += DOUBLE_SHA256(hashPrevouts)
    hashSequence = ''
    for input in vin:
        hashSequence += struct.pack('<I', input['sequence']).hex()
    hashSequence = DOUBLE_SHA256(hashSequence)
    res += hashSequence
    # outpoint
    res += hex_to_little_endian(vin[idx]['txid'])
    res += struct.pack('<I', vin[idx]['vout']).hex()
    # scriptCode
    # And then the scriptCode, which, in P2WPKH’s case, is 1976a914 <pubkey hash> 88ac 
    pub_key_hash = vin[idx]['prevout']['scriptpubkey_asm'].split(" ")[2]
    scriptcode = '1976a914' + pub_key_hash + '88ac'
    res += scriptcode
    # value of the output spent by this input
    res += struct.pack('<Q', vin[idx]['prevout']['value']).hex()
    # nSequence of the input
    res += struct.pack('<I', vin[idx]['sequence']).hex()
    # hashOutputs
    hashOutputs = ''
    for output in vout:
        hashOutputs += struct.pack('<Q', output['value']).hex()
        hashOutputs += struct.pack("<B", ((len(output['scriptpubkey']))//2)).hex()
        hashOutputs += output['scriptpubkey']
    res += DOUBLE_SHA256(hashOutputs)
    # nLocktime of the transaction
    res += struct.pack('<I', locktime).hex()
    # sighash type of the signature
    res += '01000000'
    return res



class Transaction:
    def __init__(self, json_data) -> None:
        data_dict = json.loads(json_data)  # Convert JSON string to dictionary
        self.version = data_dict.get("version")
        self.locktime = data_dict.get("locktime")
        self.vin = data_dict.get("vin")
        self.vout = data_dict.get("vout")
        self.is_coinbase = False

    def print_transaction(self):
        print(f"Version: {self.version}")
        print(f"Locktime: {self.locktime}")
        print("Vin:")
        for input in self.vin:
            print(input)
        print("Vout:")
        for output in self.vout:
            print(output)

    '''
    Steps:
     1. nVersion of the transaction (4-byte little endian)
     2. hashPrevouts (32-byte hash)
     3. hashSequence (32-byte hash)
     4. outpoint (32-byte hash + 4-byte little endian) 
     5. scriptCode of the input (serialized as scripts inside CTxOuts)
     6. value of the output spent by this input (8-byte little endian)
     7. nSequence of the input (4-byte little endian)
     8. hashOutputs (32-byte hash)
     9. nLocktime of the transaction (4-byte little endian)
    10. sighash type of the signature (4-byte little endian)
    '''
    

    def validate(self):
        # checking the pubscript type
        cnt = 0
        for input in self.vin:
            if input['prevout']['scriptpubkey_type'] != 'v0_p2wpkh':
                cnt += 1
        
        if cnt > 0:
            return False

        for idx, input in enumerate(self.vin):
            if input['prevout']['scriptpubkey_type'] == 'v0_p2wpkh':
                trimmed_tx = serialize(self.version, self.locktime, self.vin, self.vout, idx)
                message = hashlib.sha256(bytes.fromhex(trimmed_tx)).digest()
                print(message)
                signature = input['witness'][0]
                public_key = input['witness'][-1]
                if OP_CHECKSIG(signature, public_key, message) == False:
                    print('Signature verification failed') 
                
        

        # print(self.vin[0]['txid'])
        total_input = 0
        for input in self.vin:
            total_input += input['prevout']['value']
        total_output = 0
        for output in self.vout:
            total_output += output['value']
        if total_input <= total_output:
            print('Insufficient funds')
            return False
        return True
    
tx = Transaction(json.dumps(data))
print(tx.validate())

print(OP_HASH160('0300af51fb8f6ecb4a3a26b5d0b542e9ec0a660581c6e65c820184bfb052d3422b'))