from turtle import color
import pandas as df
import matplotlib.pyplot as plt
from sklearn.metrics import log_loss

df = df.read_csv('bybit_computed_adjusted.csv')

BYBIT_MIN = 10
LOOKBACK = 300
MIN_WIN = 0.2 # in %
CON = 100

wins = 0
loss = 0
last = 0

for i in range(1,len(df.ratiodp)):
    cur = df.ratiodp[i-1]

    if df.ratiodp[i-1] > BYBIT_MIN and i > last + CON:
        print(f"\nBuy {cur} {df.ratiodp[i]}")
        last = i

        maxx = ((max(df.Price.loc[i:i+LOOKBACK])-(df.Price.loc[i]))/(df.Price.loc[i]))*100
        minn = ((min(df.Price.loc[i:i+LOOKBACK])-(df.Price.loc[i]))/(df.Price.loc[i]))*100

        print(f"MAX: {maxx}")
        print(f"MIN: {minn}")

        plt.plot(df.Price.loc[i:i+LOOKBACK], color='green')
        plt.show()

    elif df.ratiodp[i-1] < -BYBIT_MIN and i > last + CON:
        print(f"\nSell {cur} {df.ratiodp[i]}")
        last = i

        maxx = ((max(df.Price.loc[i:i+LOOKBACK])-(df.Price.loc[i]))/(df.Price.loc[i]))*100
        minn = ((min(df.Price.loc[i:i+LOOKBACK])-(df.Price.loc[i]))/(df.Price.loc[i]))*100

        print(f"MAX: {maxx}")
        print(f"MIN: {minn}")

        plt.plot(df.Price.loc[i:i+LOOKBACK], color='red')
        plt.show()

print(f"WINS: {wins}")
print(f"LOSS: {loss}")