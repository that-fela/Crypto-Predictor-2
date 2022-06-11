from cProfile import run
from matplotlib import ticker
from pyparsing import line
import yfinance as yf
import asyncio

async def getPercent(starting_price, ending_price):
    return (ending_price/starting_price)*100

async def getPercentagChange(ticker, i):
    ticker = yf.Ticker(ticker)
    data = ticker.history(interval='1d', period='1mo')
    closing_prices = data['Close']
    if len(closing_prices) > 0:
        perc_change = await getPercent(closing_prices[0], closing_prices[-1])
    else:
        perc_change = 0

    change[i] = perc_change

async def run():
    for t in range(0,len(tickers)):
        await asyncio.gather(getPercentagChange(tickers[t], index[t]))
        print(f"{t}/{len(tickers)}")

if __name__ == "__main__":
    lines = []
    with open("corp_ticks_yf.txt", 'r') as f:
        lines = f.readlines()

    tickers = []
    for l in lines:
        if l.find('.') == -1:
            tickers.append(l[0:-1])

    index = [i for i in range(len(tickers))]
    change = []
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    loop.close()

    print(change)