# from utils import *
import hashlib

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

txids = ['d7bb952d73cce047178953c242bf0445362188901f2c855ea47cb9736589c848',
'529d9478511a587d81cde63933552f702074187e39223a35966d72e4dcf3b3b7',
'e7599201cc39f4d5c1ada0875ebfce3d361dacf2b7de7b37bfe16f2bdacc58d0',
'4891006444918b895fd13ec97d4b7d671141e0675b9d64fc751b5b1be7d4c3cd',
'512a462521cf2221911e06dd58fe975ff1511460cf4d14d441e9a40b4cc203fe',
'e54edbd3902c01f154112001a51ac5c6b1847bc8e80279abb2f51fc1f827c5e6',
'e4a1b1f85ba8d3bdb77397e30055fc02f18a4affa2f8baeb7c377ccc0cc2d244',
'e2cd5463424e7c2ffd6cec1c81621d20bfe1b7741ff1548574ac299b2e65eba1',
'41671c742a150a339237ee364a18347cc82273d67013b82648ff7c0c029ada9f',
'68bb0c532ce0a655023a8fd4dd061ff26daa53008ce716557c83ec76859a6f1f']


merkle_root = get_merkle_root(txids)
print(merkle_root)

s = "04000000e16692b41c752cd85e4839c5664806dfc8aa468ea74da00200000000000000002ab2f3b9054f45a53dd38d3548b55283f8c652ebc68447b8ca18ed6f4113a882b4fbf456c3a406186a82ba0c"
# print(DOUBLE_SHA256(s))