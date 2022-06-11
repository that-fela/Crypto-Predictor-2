import ai
import pandas as df
import matplotlib.pyplot as plt

df = df.read_csv('deltaPriceBybit.csv')

BYBIT_MIN = 4
BINANCE_MIN = 0.15
BITFINEX_MIN = 1
LOOKBACK = 500

for i in range(len(df.deltaBybit)):
    if df.deltaBybit[i] > BYBIT_MIN:
        print(f"MAX: {((max(df.price.loc[i:i+LOOKBACK])-min(df.price.loc[i:i+LOOKBACK]))/min(df.price.loc[i:i+LOOKBACK]))*100}")
        print(f"MIN: {((min(df.price.loc[i:i+LOOKBACK])-max(df.price.loc[i:i+LOOKBACK]))/max(df.price.loc[i:i+LOOKBACK]))*100}")
        plt.plot(df.price.loc[i:i+LOOKBACK])
        plt.show()

