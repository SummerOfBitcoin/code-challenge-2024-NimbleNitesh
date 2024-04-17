import os
import json
from test import Transaction


directory = '../mempool'
ans = 0

for filename in os.listdir(directory):
    if filename.endswith(".json"):
        with open(os.path.join(directory, filename)) as f:
            data = json.load(f)
            tx = Transaction(json.dumps(data))
            if tx.validate():
                ans+=1
                # print(f'{filename} is valid')
            # else:
            #     print(f'{filename} is invalid')
            # break
print(ans)