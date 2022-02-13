import asyncio
from threading import Timer
import time

class orderBook:
    buys = []
    sells = []
    times = []

    def __init__(self, buys, sells) -> None:
        self.buys.append(buys)
        self.sells.append(sells)
        self.times.append(time.time())

returns = [orderBook]*4
# 0 = bybit
# 1 = binance
# 2 = ftx
# 3 = bitfinex

async def getBybit():
    pass

async def getBinance():
    pass

async def getFTX():
    pass

async def getBitfinex():
    pass

async def runOrderbook():
    await asyncio.gather(getBybit(), getBinance(), getFTX(), getBitfinex())

if __name__ == "__main__":
    s = time.perf_counter()
    asyncio.run(runOrderbook())
    print(time.perf_counter() - s)

    print(returns)
