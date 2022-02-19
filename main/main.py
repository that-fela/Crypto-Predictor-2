import asyncio
from threading import Timer
import time
from urllib.request import urlopen
import json
import urllib
import datetime as dt

pBoundry = 1.01 #

returns = [0]*3
tBuys = [0]*3
tSell = [0]*3
tPrice = 0
# 0 = bybit
# 1 = binance
# 2 = bitfinex

async def getURL(url):
    req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"}) 
    con = urllib.request.urlopen(req) 

    data = con.read().decode('utf-8')
    jdata = json.loads(data)
    return jdata

async def getBybit():
    data = await getURL('https://api-testnet.bybit.com/v2/public/orderBook/L2?symbol=ETHUSDT')

    buys = 1.0
    sell = 1.0
    for res in data["result"]:
        if (float(res["price"]) < tPrice * pBoundry and float(res["price"]) > tPrice * (pBoundry - 1)):
            if (res["side"] == "Buy"): buys += float(res["size"])
            else: sell += float(res["size"])

    returns[0] = buys / sell
    tBuys[0] = buys
    tSell[0] = sell

async def getBinance():
    data = await getURL('https://api.binance.com/api/v3/depth?symbol=ETHUSDT&limit=1000')

    buys = 1.0
    sell = 1.0
    for bid in data["bids"]:
        if (float(bid[0]) < tPrice * pBoundry and float(bid[0]) > tPrice * (pBoundry - 1)): buys += float(bid[1])
    for ask in data["asks"]:
        if (float(ask[0]) < tPrice * pBoundry and float(ask[0]) > tPrice * (pBoundry - 1)):sell += float(ask[1])
        
    returns[1] = buys / sell
    tBuys[1] = buys
    tSell[1] = sell

async def getBitfinex():
    data = await getURL('https://api-pub.bitfinex.com/v2/book/tETHUSD/P1/')

    buys = 1.0
    sell = 1.0
    for i in data:
        if (float(i[0]) < tPrice * pBoundry and float(i[0]) > tPrice * (pBoundry - 1)):
            if i[2] > 0: buys += float(i[2])
            else: sell += float(i[2])
    
    sell *= -1
    returns[2] = buys / sell
    tBuys[2] = buys
    tSell[2] = sell

async def getPrice():
    data = await getURL('https://api-testnet.bybit.com/v2/public/tickers?symbol=ETHUSDT')
    global tPrice
    tPrice = float(data["result"][0]["last_price"])

async def runOrderbook():
    await asyncio.gather(getBybit()
    , getBinance()
    , getBitfinex()
    , getPrice())
    

if __name__ == "__main__":
    while(True):
        s = time.perf_counter()
        asyncio.run(runOrderbook())
        print(f"------------------\nTtC: {time.perf_counter() - s:.3f}")

        for i in range(0,3):
            print(f" {returns[i]:.2f}\t{tBuys[i]:.0f}\t{tSell[i]:.0f}")
        print(f"Mean ratio: {sum(returns)/len(returns):.3f}")
        print(f"Current Price: {tPrice:.2f}")

        with open('data.txt', 'a') as writer:
            writer.write(f"{dt.datetime.now()},{tPrice},{returns[0]},{returns[1]},{returns[2]}\n")

        time.sleep(1)
