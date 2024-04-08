import os
import json
from transaction import Transaction

directory = '../mempool'
for filename in os.listdir(directory):
    if filename.endswith(".json"):
        with open(os.path.join(directory, filename)) as f:
            data = json.load(f)
            tx = Transaction(json.dumps(data))
            if tx.validate():
                print(f'{filename} is valid')
            # else:
            #     print(f'{filename} is invalid')
            # break