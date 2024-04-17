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
            if input['prevout']['scriptpubkey_type'] != 'p2pkh' and input['prevout']['scriptpubkey_type'] != 'p2sh':
                cnt += 1
        
        if cnt > 0:
            return False

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
                    # print('Public key hash mismatch')
                    return False
                
                trimmed_tx = get_trimmed_transaction_p2pkh(self.version, self.locktime, self.vin, self.vout, idx)
                message = hashlib.sha256(bytes.fromhex(trimmed_tx)).digest()

                if OP_CHECKSIG(signature, public_key, message)==False:
                    # print('Signature verification failed')
                    return False
                
            elif input['prevout']['scriptpubkey_type'] == 'p2sh':
                scriptsig_asm = input['scriptsig_asm'].split(' ')
                prevout_scriptpubkey_asm = input['prevout']['scriptpubkey_asm'].split(' ')
                redeem_script_asm = input['inner_redeemscript_asm'].split(' ')

                redeem_script = scriptsig_asm[-1]
                sh = prevout_scriptpubkey_asm[2] # script hash

                # OP_HASH160 OP_PUSHBYTES_20 <script_hash> OP_EQUAL
                hashed_redeem_script = OP_HASH160(redeem_script)
                if hashed_redeem_script != sh:
                    # print('Script hash mismatch')
                    return False

                if redeem_script_asm[-1] != 'OP_CHECKMULTISIG':
                    # No further execution needed as it is not a multisig script
                    return True
                
                # OP_PUSHNUM_2 <public_key1> <public_key2> OP_PUSHNUM_2 OP_CHECKMULTISIG

                public_keys = []
                signatures = []

                for i in redeem_script_asm:
                    if i[0:3] == 'OP_':
                        continue
                    assert(len(i) == 66)
                    public_keys.append(i)

                for i in range(len(scriptsig_asm)-1):
                    if scriptsig_asm[i][0:3] == 'OP_':
                        continue
                    signatures.append(scriptsig_asm[i])

                trimmed_tx = get_trimmed_transaction_p2sh(self.version, self.locktime, self.vin, self.vout, idx)
                message = hashlib.sha256(bytes.fromhex(trimmed_tx)).digest()

                n = redeem_script_asm[0].split('_')[-1]
                n = int(n)

                if OP_CHECKMULTISIG(n, signatures, public_keys, message)==False:
                    # print('Multisig verification failed')
                    return False

        
        return True