import json
import asyncio

class dataObject:
    prices = []
    sizes = [] # in eth

    def __init__(self) -> None:
        pass

    def set(self, prices, sizes):
        self.prices = float(prices)
        self.sizes = float(sizes)

    def setP(self, price, size):
        self.prices.append(float(price))
        self.sizes.append(float(size))
    

def loadObj(filename, convert=True):
    r = open(filename, 'r')
    data = r.readlines()

    jdata = []
    for str in data:
        if convert:          
            jdata.append(json.loads(str.replace("\'","\"")))
        else:
            jdata.append(json.loads(str))

    return jdata

def inv(s):
    p = float(s)
    p *= -1
    return str(p)

async def loadBybit(jdata):
    objs = []
    for ts in jdata:
        obj = dataObject()
        for result in ts["result"]:
            if result["side"] == "Buy": obj.setP(result["price"], result["size"])
            else: obj.setP(result["price"], inv(result["size"]))
        objs.append(obj)    

    return objs

async def AsyncTasker():
    await asyncio.gather(loadBybit())

if __name__ == "__main__":
    bybit = []

    jbybit = loadObj("_bybit.txt")
    bybit = loadBybit(jbybit)

    pass
