import os
import json
from transaction import Transaction
from construct_block import construct_block


directory = '../mempool'
valid_transactions = []

for filename in os.listdir(directory):
    if filename.endswith(".json"):
        with open(os.path.join(directory, filename)) as f:
            data = json.load(f)
            tx = Transaction(json.dumps(data))
            if tx.validate():
                valid_transactions.append(tx)
                # print(f'{filename} is valid')

construct_block(valid_transactions, block_reward=6, transaction_fee=1)