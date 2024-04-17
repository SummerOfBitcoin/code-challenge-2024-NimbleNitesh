from utils import *

data = {
  "version": 2,
  "locktime": 0,
  "vin": [
    {
      "txid": "1fba67ce9100df40f19ccb4d4062893b3c27987b9cbecf76311cbe554527e39b",
      "vout": 2,
      "prevout": {
        "scriptpubkey": "a9149cd03e792c7004be9aa5005d46653f28268416db87",
        "scriptpubkey_asm": "OP_HASH160 OP_PUSHBYTES_20 9cd03e792c7004be9aa5005d46653f28268416db OP_EQUAL",
        "scriptpubkey_type": "p2sh",
        "scriptpubkey_address": "3FzAoX2s7GhrZUZR4WXs1CvTKUGd7Ze6YM",
        "value": 1380629466
      },
      "scriptsig": "004730440220223ab514db7dc474fb3f4734f26fa8ba45cb7f5086972b9ffad31fa0548a15b9022043f38bec2672ddfc8bea2bb22637897b65a893fe27970fb0147c01bc7ee3d1540147304402206e7353155483343dbed44808d8ea48f643ee015e257797a22d4712e02e2cf3d702204824ba9a16398823b1f50ef1643ecef5daf1a5723bd1f7a241c9557743747a6b014c6952210395f33d5a959556ba6b57298066baf468c2e5ab3cc58ddaf7166f057fae1655a7210246aae217f1102dde12a7e77203f7114de07f0068cfb1a3d825fff4ca2266737621028ace79c534a3b5c482b6cc446ea20d757e88c516ec054ae31c7a47863864904853ae",
      "scriptsig_asm": "OP_0 OP_PUSHBYTES_71 30440220223ab514db7dc474fb3f4734f26fa8ba45cb7f5086972b9ffad31fa0548a15b9022043f38bec2672ddfc8bea2bb22637897b65a893fe27970fb0147c01bc7ee3d15401 OP_PUSHBYTES_71 304402206e7353155483343dbed44808d8ea48f643ee015e257797a22d4712e02e2cf3d702204824ba9a16398823b1f50ef1643ecef5daf1a5723bd1f7a241c9557743747a6b01 OP_PUSHDATA1 52210395f33d5a959556ba6b57298066baf468c2e5ab3cc58ddaf7166f057fae1655a7210246aae217f1102dde12a7e77203f7114de07f0068cfb1a3d825fff4ca2266737621028ace79c534a3b5c482b6cc446ea20d757e88c516ec054ae31c7a47863864904853ae",
      "is_coinbase": False,
      "sequence": 4294967295,
      "inner_redeemscript_asm": "OP_PUSHNUM_2 OP_PUSHBYTES_33 0395f33d5a959556ba6b57298066baf468c2e5ab3cc58ddaf7166f057fae1655a7 OP_PUSHBYTES_33 0246aae217f1102dde12a7e77203f7114de07f0068cfb1a3d825fff4ca22667376 OP_PUSHBYTES_33 028ace79c534a3b5c482b6cc446ea20d757e88c516ec054ae31c7a478638649048 OP_PUSHNUM_3 OP_CHECKMULTISIG"
    },
    {
      "txid": "e33a5b1a6e658904b783deb7ba64cb2e7987f2d6cd5bd24d223a0a71d038b288",
      "vout": 3,
      "prevout": {
        "scriptpubkey": "a9149cd03e792c7004be9aa5005d46653f28268416db87",
        "scriptpubkey_asm": "OP_HASH160 OP_PUSHBYTES_20 9cd03e792c7004be9aa5005d46653f28268416db OP_EQUAL",
        "scriptpubkey_type": "p2sh",
        "scriptpubkey_address": "3FzAoX2s7GhrZUZR4WXs1CvTKUGd7Ze6YM",
        "value": 1337178870
      },
      "scriptsig": "00483045022100be8371f6121556e1297303c328ebc987655c5ea0026e8613db0b627351ebde8d02200ed2d522a2107656736a8b28b4e5706a837e4fec5f750b2a8ebbbe416b34b154014730440220388acbdeecc2b7344199a08592a32d5b3714569a90c8f1c9e383a70c1929253102200865cad74e1c76dde824ced51d60dfff80be1df8f3009c8e188946686ec046d2014c6952210395f33d5a959556ba6b57298066baf468c2e5ab3cc58ddaf7166f057fae1655a7210246aae217f1102dde12a7e77203f7114de07f0068cfb1a3d825fff4ca2266737621028ace79c534a3b5c482b6cc446ea20d757e88c516ec054ae31c7a47863864904853ae",
      "scriptsig_asm": "OP_0 OP_PUSHBYTES_72 3045022100be8371f6121556e1297303c328ebc987655c5ea0026e8613db0b627351ebde8d02200ed2d522a2107656736a8b28b4e5706a837e4fec5f750b2a8ebbbe416b34b15401 OP_PUSHBYTES_71 30440220388acbdeecc2b7344199a08592a32d5b3714569a90c8f1c9e383a70c1929253102200865cad74e1c76dde824ced51d60dfff80be1df8f3009c8e188946686ec046d201 OP_PUSHDATA1 52210395f33d5a959556ba6b57298066baf468c2e5ab3cc58ddaf7166f057fae1655a7210246aae217f1102dde12a7e77203f7114de07f0068cfb1a3d825fff4ca2266737621028ace79c534a3b5c482b6cc446ea20d757e88c516ec054ae31c7a47863864904853ae",
      "is_coinbase": False,
      "sequence": 4294967295,
      "inner_redeemscript_asm": "OP_PUSHNUM_2 OP_PUSHBYTES_33 0395f33d5a959556ba6b57298066baf468c2e5ab3cc58ddaf7166f057fae1655a7 OP_PUSHBYTES_33 0246aae217f1102dde12a7e77203f7114de07f0068cfb1a3d825fff4ca22667376 OP_PUSHBYTES_33 028ace79c534a3b5c482b6cc446ea20d757e88c516ec054ae31c7a478638649048 OP_PUSHNUM_3 OP_CHECKMULTISIG"
    }
  ],
  "vout": [
    {
      "scriptpubkey": "76a91400fae4774da408bfd5c483e5b44cc7a8c7ce93d288ac",
      "scriptpubkey_asm": "OP_DUP OP_HASH160 OP_PUSHBYTES_20 00fae4774da408bfd5c483e5b44cc7a8c7ce93d2 OP_EQUALVERIFY OP_CHECKSIG",
      "scriptpubkey_type": "p2pkh",
      "scriptpubkey_address": "116BZK8yqkKS9YQ7SGfKGJ92oZcnymEWq5",
      "value": 1603221518
    },
    {
      "scriptpubkey": "76a914251f99100ab56057b1944aa5300a67670a290ffc88ac",
      "scriptpubkey_asm": "OP_DUP OP_HASH160 OP_PUSHBYTES_20 251f99100ab56057b1944aa5300a67670a290ffc OP_EQUALVERIFY OP_CHECKSIG",
      "scriptpubkey_type": "p2pkh",
      "scriptpubkey_address": "14PHrZPPFgzusKLAThaAs7jsk7o66de428",
      "value": 916810
    },
    {
      "scriptpubkey": "a9149cd03e792c7004be9aa5005d46653f28268416db87",
      "scriptpubkey_asm": "OP_HASH160 OP_PUSHBYTES_20 9cd03e792c7004be9aa5005d46653f28268416db OP_EQUAL",
      "scriptpubkey_type": "p2sh",
      "scriptpubkey_address": "3FzAoX2s7GhrZUZR4WXs1CvTKUGd7Ze6YM",
      "value": 1113656311
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
            if input['prevout']['scriptpubkey_type'] != 'p2sh':
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
                # print(trimmed_tx)
                if OP_CHECKSIG(signature, public_key, message)==False:
                    print('Signature verification failed')
                    return False
            
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
            
# obj = Transaction(json.dumps(data))
# print(obj.validate())
















































































































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