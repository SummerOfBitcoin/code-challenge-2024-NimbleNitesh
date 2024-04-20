import os
import json
from transaction import Transaction
from construct_block import construct_block


directory = '../mempool'
valid_transactions = []
ans = 0
tr = 0


for filename in os.listdir(directory):
    if filename.endswith(".json"):
        with open(os.path.join(directory, filename)) as f:
            data = json.load(f)
            tx = Transaction(json.dumps(data))
            if tx.validate():
                valid_transactions.append(tx)
                ans += 1
                # print(f'{filename} is valid')

print(ans)

def sort_transactions(valid_transactions):
    valid_transactions.sort(key=lambda x: str(x.vin[0]['txid']))
    return valid_transactions

sort_transactions(valid_transactions)
valid_transactions = valid_transactions[:2400]

# for i in range(5):
#     print(valid_transactions[i].vin[0]['txid'])

construct_block(valid_transactions, block_reward=6, transaction_fee=1)