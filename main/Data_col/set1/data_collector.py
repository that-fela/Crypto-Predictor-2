import asyncio
from threading import Timer
import time
from urllib.request import urlopen
import json
import urllib
import datetime as dt
import pickle

# 0 = bybit
# 1 = binance
# 2 = bitfinex

async def getURL(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    con = urllib.request.urlopen(req)

    data = con.read().decode('utf-8')
    jdata = json.loads(data)
    return jdata

async def getBybit():
    jdata = await getURL('https://api-testnet.bybit.com/v2/public/orderBook/L2?symbol=ETHUSDT')
    with open('_bybit.txt', 'a') as w:
         w.write(f"{str(jdata)}\n")
    print("Bybit Done")

async def getBinance():
   jdata = await getURL('https://api.binance.com/api/v3/depth?symbol=ETHUSDT&limit=100')
   with open('_binance.txt', 'a') as w:
         w.write(f"{str(jdata)}\n")
   print("Binance Done")

async def getBitfinex():
    jdata = await getURL('https://api-pub.bitfinex.com/v2/book/tETHUSD/P1/')
    with open('_bitfinex.txt', 'a') as w:
         w.write(f"{str(jdata)}\n")
    print("Bitfinex Done")

async def getPrice():
    jdata = await getURL('https://api-testnet.bybit.com/v2/public/tickers?symbol=ETHUSDT')
    with open('_price.txt', 'a') as w:
         w.write(f"{str(jdata)}\n")
    print("Price Done")

    global tPrice
    tPrice = float(jdata["result"][0]["last_price"])

async def runOrderbook():
    await asyncio.gather(getBybit()
    , getBinance()
    , getBitfinex()
    , getPrice())
    

if __name__ == "__main__":
    tPrice = 0
    
    index = 1
    start = dt.datetime.now()
    while(True):
        try:
            s = time.perf_counter()
            asyncio.run(runOrderbook())
            print(f"{index} \tTtC: {time.perf_counter() - s:.3f} \tCurrent Price: {tPrice:.2f} \t{dt.datetime.now() - start} \t{dt.datetime.now()}")

            time.sleep(1.1)
            index += 1
        except:
            pass


# import asynio
