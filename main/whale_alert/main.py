import time
from pprint import pprint
from tkinter import W
from whalealert.whalealert import WhaleAlert
import datetime as dt
import time

start_time = int(time.time() - 1500)
whale = WhaleAlert()
api_key = 'mIl5xKVgcxPoo5pfF7JUREkFwq0dDlGw'

prev = []

while True:
    success, transactions, status = whale.get_transactions(start_time, api_key=api_key)
    for tran in transactions:
        if (tran['blockchain'] == 'bitcoin' or tran['blockchain'] == 'ethereum') and tran['amount_usd'] > 1500000 and (tran['from']['owner_type'] == 'exchange' or tran['to']['owner_type'] == 'exchange') and (tran not in prev):
            print(f"Amount {tran['amount_usd']}, Time: {dt.datetime.fromtimestamp(tran['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}, Blockchain: {tran['blockchain']}, DEST: {tran['from']['owner_type']} -> {tran['to']['owner_type']}")
            prev.append(tran)
    
    time.sleep(10)