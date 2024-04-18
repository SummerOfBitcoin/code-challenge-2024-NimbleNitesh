from utils import *

data = {
  "version": 1,
  "locktime": 0,
  "vin": [
    {
      "txid": "c0bfed04919d5f9591eab67e723d37bf78b06279bcc01efb971a9cd99460f9e2",
      "vout": 1,
      "prevout": {
        "scriptpubkey": "76a9143f41884dda2604ddb09fe015da88d6345b91369b88ac",
        "scriptpubkey_asm": "OP_DUP OP_HASH160 OP_PUSHBYTES_20 3f41884dda2604ddb09fe015da88d6345b91369b OP_EQUALVERIFY OP_CHECKSIG",
        "scriptpubkey_type": "p2pkh",
        "scriptpubkey_address": "16mU5MpSAXMSF7gnmYxEzBY5vWyQeQaS43",
        "value": 72045507415
      },
      "scriptsig": "483045022100bfa227baae7f67e9077b8f35d57d378d8f98e30d593f98d1ab5b152ba3fa41b00220200d07f3279b0c4b9147bb5ff91a3b70b97ffdbbd58ae29b907c3ab58e87e55801210278f837d426608340ed98f6502f5b93569391b2fe6a6f0a8e1bafe7612db6b47d",
      "scriptsig_asm": "OP_PUSHBYTES_72 3045022100bfa227baae7f67e9077b8f35d57d378d8f98e30d593f98d1ab5b152ba3fa41b00220200d07f3279b0c4b9147bb5ff91a3b70b97ffdbbd58ae29b907c3ab58e87e55801 OP_PUSHBYTES_33 0278f837d426608340ed98f6502f5b93569391b2fe6a6f0a8e1bafe7612db6b47d",
      "is_coinbase": False,
      "sequence": 4294967295
    }
  ],
  "vout": [
    {
      "scriptpubkey": "76a914394c3c7981e757c245362187703b4e812c6652fc88ac",
      "scriptpubkey_asm": "OP_DUP OP_HASH160 OP_PUSHBYTES_20 394c3c7981e757c245362187703b4e812c6652fc OP_EQUALVERIFY OP_CHECKSIG",
      "scriptpubkey_type": "p2pkh",
      "scriptpubkey_address": "16DxqvPCMrEyBvuMDxkc9Lgk4jYmCRbqaE",
      "value": 399000000
    },
    {
      "scriptpubkey": "76a9143f41884dda2604ddb09fe015da88d6345b91369b88ac",
      "scriptpubkey_asm": "OP_DUP OP_HASH160 OP_PUSHBYTES_20 3f41884dda2604ddb09fe015da88d6345b91369b OP_EQUALVERIFY OP_CHECKSIG",
      "scriptpubkey_type": "p2pkh",
      "scriptpubkey_address": "16mU5MpSAXMSF7gnmYxEzBY5vWyQeQaS43",
      "value": 71646495574
    }
  ]
}

'''
You will need to calculate z which is the transaction hash. To calculate this value, you will have to take the raw transaction's hexadecimal and replace all the inputs ScriptSigs with the redeem script + SIGHASH_ALL ("01000000" in hexadecimal). After you do this, you apply a double sha256 (also called Hash256), and that's it. You have your z. With this value you can check an individual signature and evaluate it against all the public keys from the redeem script but one by one. A signature is a pair of values (r,s). The formula you will have to evaluate is: 

'''

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
            if input['prevout']['scriptpubkey_type'] != 'p2pkh':
                cnt += 1
        
        if cnt > 0:
            return False
        
        # for idx, input in enumerate(self.vin):
        #     if input['prevout']['scriptpubkey_type'] == 'p2sh':
        #         trimmed_tx = get_message(self.version, self.locktime, self.vin, self.vout, idx)
        #         # print(trimmed_tx)
        #         message = hashlib.sha256(bytes.fromhex(trimmed_tx)).digest()
        #         # print(message.hex())

        # public_keys = ['029640a253abbf6252e6d195882262da255d6dd17e66cd8aca2610083f6d4d1781', '03a553e30733d7a8df6d390d59cc136e2c9d9cf4e808f3b6ab009beae68dd60822', '03211aec906e232ad96f2d52e849cf2798f4cf2d3d3463f608a7638054542defd6']
        # signatures = ['3044022061f5cb2c6a6638e40c7235b888224c6352ea1fe60bd5af6e52b2d77453279ebf0220175360ad1aa5d6f612e19eaa75e155e37a8de938f84985a1bf1220148e20a18301', '3044022065b884e14705c85b462b41fdfe295f4f0e53baf780840b30c0b90f71833dd64d02206ac04c63828ba80e274c4ff96a03f39f450b4bedcb70b415047ea1ee7c71257001']

        # for public_key in public_keys:
        #   for signature in signatures:
        #       if OP_CHECKSIG(signature, public_key, message):
        #           print(f'Public key: {public_key} Signature: {signature} is valid')

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
                
                trimmed_tx = get_trimmed_transaction_p2pkh(self.version, self.locktime, self.vin, self.vout, idx)
                message = hashlib.sha256(bytes.fromhex(trimmed_tx)).digest()
                print(message.hex())
                if OP_CHECKSIG(signature, public_key, message)==False:
                    print('Signature verification failed')
                    return False
            
                # return True
            elif input['prevout']['scriptpubkey_type'] == 'p2sh':
                scriptsig_asm = input['scriptsig_asm'].split(' ')
                prevout_scriptpubkey_asm = input['prevout']['scriptpubkey_asm'].split(' ')

                redeem_script = scriptsig_asm[-1]
                pkh = prevout_scriptpubkey_asm[2]
                # print(redeem_script)
                hashed_value = OP_HASH160(redeem_script)
                if hashed_value != pkh:
                    print('Public key hash mismatch')
                    return False
                
                redeem_script_asm = input['inner_redeemscript_asm'].split(' ')
                if redeem_script_asm[-1] != 'OP_CHECKMULTISIG':
                    # print(redeem_script_asm[-1])
                    return True
                
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

                # print(public_keys)
                # print(signatures)

                trimmed_tx = get_trimmed_transaction_p2sh(self.version, self.locktime, self.vin, self.vout, idx)
                message = hashlib.sha256(bytes.fromhex(trimmed_tx)).digest()
                # print(trimmed_tx)

                n = redeem_script_asm[0].split('_')[-1]
                n = int(n)
                # print(n)

                for public_key in public_keys:
                    for signature in signatures:
                        if OP_CHECKSIG(signature, public_key, message):
                            n -= 1
                            # print(f'Public key: {public_key} Signature: {signature} is valid')
                            signatures.remove(signature)
                            public_keys.remove(public_key)

                if n > 0:
                    print(f'Signature verification failed {n} remaining txid {input["txid"]}')

                    return False 
        print(f'Transaction is valid txid {input["txid"]}')
        return True
            
obj = Transaction(json.dumps(data))
print(obj.validate())














































































































'''
p2pkh:
{
  "version": 2,
  "locktime": 0,
  "vin": [
    {
      "txid": "fb7fe37919a55dfa45a062f88bd3c7412b54de759115cb58c3b9b46ac5f7c925",
      "vout": 1,
      "prevout": {
        "scriptpubkey": "76a914286eb663201959fb12eff504329080e4c56ae28788ac",
        "scriptpubkey_asm": "OP_DUP OP_HASH160 OP_PUSHBYTES_20 286eb663201959fb12eff504329080e4c56ae287 OP_EQUALVERIFY OP_CHECKSIG",
        "scriptpubkey_type": "p2pkh",
        "scriptpubkey_address": "14gnf7L2DjBYKFuWb6iftBoWE9hmAoFbcF",
        "value": 433833
      },
      "scriptsig": "4830450221008f619822a97841ffd26eee942d41c1c4704022af2dd42600f006336ce686353a0220659476204210b21d605baab00bef7005ff30e878e911dc99413edb6c1e022acd012102c371793f2e19d1652408efef67704a2e9953a43a9dd54360d56fc93277a5667d",
      "scriptsig_asm": "OP_PUSHBYTES_72 30450221008f619822a97841ffd26eee942d41c1c4704022af2dd42600f006336ce686353a0220659476204210b21d605baab00bef7005ff30e878e911dc99413edb6c1e022acd01 OP_PUSHBYTES_33 02c371793f2e19d1652408efef67704a2e9953a43a9dd54360d56fc93277a5667d",
      "is_coinbase": False,
      "sequence": 4294967295
    }
  ],
  "vout": [
    {
      "scriptpubkey": "76a9141ef7874d338d24ecf6577e6eadeeee6cd579c67188ac",
      "scriptpubkey_asm": "OP_DUP OP_HASH160 OP_PUSHBYTES_20 1ef7874d338d24ecf6577e6eadeeee6cd579c671 OP_EQUALVERIFY OP_CHECKSIG",
      "scriptpubkey_type": "p2pkh",
      "scriptpubkey_address": "13pjoLcRKqhzPCbJgYW77LSFCcuwmHN2qA",
      "value": 387156
    },
    {
      "scriptpubkey": "76a9142e391b6c47778d35586b1f4154cbc6b06dc9840c88ac",
      "scriptpubkey_asm": "OP_DUP OP_HASH160 OP_PUSHBYTES_20 2e391b6c47778d35586b1f4154cbc6b06dc9840c OP_EQUALVERIFY OP_CHECKSIG",
      "scriptpubkey_type": "p2pkh",
      "scriptpubkey_address": "15DQVhQ7PU6VPsTtvwLxfDsTP4P6A3Z5vP",
      "value": 37320
    }
  ]
}


p2sh:
{
  "version": 2,
  "locktime": 0,
  "vin": [
    {
      "txid": "090ae4cb35569806cc1ac24d0bafb031b8faaa78b87fc91170d8323e3ce8fad9",
      "vout": 0,
      "prevout": {
        "scriptpubkey": "a9142c21151d54bd219dcc4c52e1cb38672dab8e36cc87",
        "scriptpubkey_asm": "OP_HASH160 OP_PUSHBYTES_20 2c21151d54bd219dcc4c52e1cb38672dab8e36cc OP_EQUAL",
        "scriptpubkey_type": "p2sh",
        "scriptpubkey_address": "35iMHbUZeTssxBodiHwEEkb32jpBfVueEL",
        "value": 13771240
      },
      "scriptsig": "1600147c846a806f4d9e516c9fb2fe364f28eac4e3c3fc",
      "scriptsig_asm": "OP_PUSHBYTES_22 00147c846a806f4d9e516c9fb2fe364f28eac4e3c3fc",
      "witness": [
        "304402205a870b4d3a918c2f26d94127436c7fb0e4484ad25bf7d3ad1db0da350c00ebbb022011a3f26ac25df4c59c3449f9be9c89652163f67025810d7ce96df35fb8e82a2901",
        "03789a9d83798d4cbf688f9969a94084ee1655059e137b43492ee94dc4538790ab"
      ],
      "is_coinbase": False,
      "sequence": 4294967295,
      "inner_redeemscript_asm": "OP_0 OP_PUSHBYTES_20 7c846a806f4d9e516c9fb2fe364f28eac4e3c3fc"
    }
  ],
  "vout": [
    {
      "scriptpubkey": "a914f4ce667f0a7b9439eca3b451b43d8e6dc690662687",
      "scriptpubkey_asm": "OP_HASH160 OP_PUSHBYTES_20 f4ce667f0a7b9439eca3b451b43d8e6dc6906626 OP_EQUAL",
      "scriptpubkey_type": "p2sh",
      "scriptpubkey_address": "3Q1S4JMASK1pMRAf8QXcQGGMBMxSRq2Nca",
      "value": 4914741
    },
    {
      "scriptpubkey": "a9142c21151d54bd219dcc4c52e1cb38672dab8e36cc87",
      "scriptpubkey_asm": "OP_HASH160 OP_PUSHBYTES_20 2c21151d54bd219dcc4c52e1cb38672dab8e36cc OP_EQUAL",
      "scriptpubkey_type": "p2sh",
      "scriptpubkey_address": "35iMHbUZeTssxBodiHwEEkb32jpBfVueEL",
      "value": 8852838
    }
  ]
}


  p2sh with multisig:
  {
  "version": 1,
  "locktime": 0,
  "vin": [
    {
      "txid": "0e52722658432b75d8e16a2f6dfca08db0eae50fd7ce32f673cac4bd0b70b544",
      "vout": 1,
      "prevout": {
        "scriptpubkey": "a914e6a63531e03db543823d0a46a4377af7de37153987",
        "scriptpubkey_asm": "OP_HASH160 OP_PUSHBYTES_20 e6a63531e03db543823d0a46a4377af7de371539 OP_EQUAL",
        "scriptpubkey_type": "p2sh",
        "scriptpubkey_address": "3NiaSz4VomF9ajkNX6H6AdFHyYWnmRWzLQ",
        "value": 645637
      },
      "scriptsig": "00473044022061f5cb2c6a6638e40c7235b888224c6352ea1fe60bd5af6e52b2d77453279ebf0220175360ad1aa5d6f612e19eaa75e155e37a8de938f84985a1bf1220148e20a18301473044022065b884e14705c85b462b41fdfe295f4f0e53baf780840b30c0b90f71833dd64d02206ac04c63828ba80e274c4ff96a03f39f450b4bedcb70b415047ea1ee7c712570014c695221029640a253abbf6252e6d195882262da255d6dd17e66cd8aca2610083f6d4d17812103a553e30733d7a8df6d390d59cc136e2c9d9cf4e808f3b6ab009beae68dd608222103211aec906e232ad96f2d52e849cf2798f4cf2d3d3463f608a7638054542defd653ae",
      "scriptsig_asm": "OP_0 OP_PUSHBYTES_71 3044022061f5cb2c6a6638e40c7235b888224c6352ea1fe60bd5af6e52b2d77453279ebf0220175360ad1aa5d6f612e19eaa75e155e37a8de938f84985a1bf1220148e20a18301 OP_PUSHBYTES_71 3044022065b884e14705c85b462b41fdfe295f4f0e53baf780840b30c0b90f71833dd64d02206ac04c63828ba80e274c4ff96a03f39f450b4bedcb70b415047ea1ee7c71257001 OP_PUSHDATA1 5221029640a253abbf6252e6d195882262da255d6dd17e66cd8aca2610083f6d4d17812103a553e30733d7a8df6d390d59cc136e2c9d9cf4e808f3b6ab009beae68dd608222103211aec906e232ad96f2d52e849cf2798f4cf2d3d3463f608a7638054542defd653ae",
      "is_coinbase": False,
      "sequence": 4294967293,
      "inner_redeemscript_asm": "OP_PUSHNUM_2 OP_PUSHBYTES_33 029640a253abbf6252e6d195882262da255d6dd17e66cd8aca2610083f6d4d1781 OP_PUSHBYTES_33 03a553e30733d7a8df6d390d59cc136e2c9d9cf4e808f3b6ab009beae68dd60822 OP_PUSHBYTES_33 03211aec906e232ad96f2d52e849cf2798f4cf2d3d3463f608a7638054542defd6 OP_PUSHNUM_3 OP_CHECKMULTISIG"
    }
  ],
  "vout": [
    {
      "scriptpubkey": "a9148c5b2b2f7352c6d417f71120b6cf184f1d02543487",
      "scriptpubkey_asm": "OP_HASH160 OP_PUSHBYTES_20 8c5b2b2f7352c6d417f71120b6cf184f1d025434 OP_EQUAL",
      "scriptpubkey_type": "p2sh",
      "scriptpubkey_address": "3EV9juqgMiqshyxT9dBnVjwoSkijRqLeh9",
      "value": 635800
    }
  ]
}


'''