from utils import *

a = 'e409711a202e7350b46d98d67ff5f3bcce30060b61c48b5aaae501f553a551ed'
b = '824c5b94c1af263b96b16fb798ef6de6cc51dd2043c7e45f50054d87292f7124'
c = '29c818dcd439bb4fc2df86751d744fb36a07ae70df301f7cf83f84970c7935fa'
txids = [a, b, c]
# for all permutation of a, b, c
for i in range(3):
    for j in range(3):
        for k in range(3):
            if i == j or j == k or k == i:
                continue
            test = [txids[i], txids[j], txids[k]]
            print(test, get_merkle_root(test))