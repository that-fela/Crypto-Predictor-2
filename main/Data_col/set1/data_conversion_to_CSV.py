import json
from struct import pack
from sys import api_version
import matplotlib.pyplot as plt
import pandas as pd

def loadJson(filename) -> json:
    lines = []
    with open(filename, 'r') as r:
        lines = r.readlines()
    
    jData = []
    for i in lines:
        jData.append(json.loads(i.replace("\'","\"")))

    return jData

def loadBybit(filename='_bybit.txt') -> None:
    print("Loading Bybit ...")
    jData = loadJson(filename)
    print("Loaded Bybit")

    for packetNum in range(len(jData)-1):
        total_buys = []
        total_sells = []
        tb = []
        ts = []
        bPrice = 0
        sPrice = 0

        for i in jData[packetNum]['result']:
            if i['side'] == "Buy": 
                tb.append(float(i['size']))
                if bPrice == 0: bPrice = float(i['price'])
            else: # side = Ask
                ts.append(float(i['size']))
                if sPrice == 0: sPrice = float(i['price'])
        
        for i in range(len(tb)):
            total_buys.append(tb[i] * ((i+1)/len(tb)))
        
        for i in range(len(ts)):
            total_sells.append(ts[i] * ((len(ts) - i+1)/len(ts)))
        
        df.Index.loc[packetNum] = packetNum
        df.Price.loc[packetNum] = (bPrice + sPrice) / 2
        try:
            if len(total_buys) >= len(total_sells): 
                df.Ratio.loc[packetNum] = sum(total_buys) / sum(total_sells) 
            else: 
                df.Ratio.loc[packetNum] = -1 * sum(total_sells) / sum(total_buys) 

            if packetNum > 0: 
                df.DeltaPrice.loc[packetNum] = (df.Price.loc[packetNum] - df.Price.loc[packetNum-1]) / df.Price.loc[packetNum-1]
            else: 
                df.DeltaPrice.loc[packetNum] = 0.0
        except:
            pass
        print(f"{packetNum} / {len(jData)-1}")

# NOT FUCKING IMPLENETED SO DONT FUCKIGN CALL IT
def loadBinance(filename='_bianance.txt') -> None:
    jData = loadJson(filename)

    for packetNum in range(len(jData)-1):
        total_buys = []
        total_sells = []

        for i in jData[packetNum]['bids']:
            total_buys.append([float(i[0]), float(i[1])])
        for i in jData[packetNum]['asks']:
            total_buys.append([float(i[0]), float(i[1])])

        df.Binance.loc[packetNum] = [total_buys, total_sells]

def getDifference(array1, array2) -> list:
    dif = []
    for i in range(len(array1)-1):
        dif.append(abs(array1[i] - array2[i]))
    
    return sum(dif)

def findConstants(DeltaPrice, Buys, Sells) -> float:
    pass

if __name__ == "__main__":

    df = pd.DataFrame(index=range(len(loadJson("_Price.txt"))), columns=['Index','Price','DeltaPrice','Ratio'])
    #df.loc[0] = 0,0,0,0
    #df.Price.loc[0] = 1
    #df.Price.at[0] = 1

    loadBybit()
    #ai.ai(pd.DataFrame(df.Index, df.DeltaPrice))
    
    #print(df.describe())
    #print(df.Price)
    #print(df.DeltaPrice)

    # formula 4 implentation
    #plt.plot(df.DeltaPrice)
    #plt.show()

    df.to_csv('bybit_computed_adjusted.csv', index=False)

