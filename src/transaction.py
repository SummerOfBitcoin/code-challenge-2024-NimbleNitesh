from utils import *

class Transaction:
    def __init__(self, json_data) -> None:
        data_dict = json.loads(json_data)  # Convert JSON string to dictionary
        self.version = data_dict.get("version")
        self.locktime = data_dict.get("locktime")
        self.vin = data_dict.get("vin")
        self.vout = data_dict.get("vout")

    def validate(self):
        # checking the pubscript type
        cnt = 0
        for input in self.vin:
            if input['prevout']['scriptpubkey_type'] == 'p2pkh':
                cnt += 1
        
        if cnt == 0:
            return False
        # print(len(self.vin))
        for idx, input in enumerate(self.vin):
            if input['prevout']['scriptpubkey_type'] == 'p2pkh':
                scriptsig_asm = input['scriptsig_asm'].split(' ')
                prevout_scriptpubkey_asm = input['prevout']['scriptpubkey_asm'].split(' ')

                public_key = scriptsig_asm[-1]
                signature = scriptsig_asm[1]
                pkh = prevout_scriptpubkey_asm[3] # public key hash

                # OP_DUP OP_HASH160 OP_PUSHBYTES_20 <public_key_hash> OP_EQUALVERIFY OP_CHECKSIG
                hashed_public_key = OP_HASH160(public_key)
                if hashed_public_key != pkh:
                    print('Public key hash mismatch')
                    return False
                
                trimmed_tx = get_trimmed_transaction(self.version, self.locktime, self.vin, self.vout, idx)
                message = hashlib.sha256(bytes.fromhex(trimmed_tx)).digest()

                if OP_CHECKSIG(signature, public_key, message)==False:
                    print('Signature verification failed')
                    return False
        return True