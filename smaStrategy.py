import datetime as dt
import pandas as pd
import numpy as np
import pandas_datareader.data as web 
import matplotlib.pyplot as plt
import mplfinance as mpf
from matplotlib import style

style.use('ggplot')
#tickers = ['AAPL', 'MSFT', 'AMZN', 'TSLA', 'FB', 'NVDA', 'JPM', 'V', 'BAC']
start = dt.datetime(2012,11,1)
end = dt.datetime(2017,12,28)
#for ticker in tickers:
df = web.DataReader(ticker, 'yahoo', start, end)

df["Date"] = df.index

#simple moving average
df['5ma'] = df['Close'].rolling(window=5).mean()
df['10ma'] = df['Close'].rolling(window=10).mean()
df['20ma'] = df['Close'].rolling(window=20).mean()
df['50ma'] = df['Close'].rolling(window=50).mean()
df['100ma'] = df['Close'].rolling(window=100).mean()
df['200ma'] = df['Close'].rolling(window=200).mean()

df['Close'].plot(label = 'Close', color='gray')
df['20ma'].plot(label = '20 day SMA',color='red')
df['50ma'].plot(label = '50 day SMA',color='blue')
#df['5ma'].plot(label = '5 day SMA',color='red')
#df['10ma'].plot(label = '10 day SMA',color='blue')

#exponential weighted moving average
# df['20dayEMA'] = df['Close'].ewm(span=20, adjust=False).mean()
# df['50dayEMA'] = df['Close'].ewm(span=50, adjust=False).mean()
# df['20dayEMA'].plot(color='purple')
# df['50dayEMA'].plot(color='green')


#df['Signal'] = np.where(df['20dayEMA'] >= df['50dayEMA'], 1, 0)

#when sma20 > sma50 return 1 else return 0
df['Signal'] = np.where(df['50ma'] <= df['20ma'], 1, 0)

#difference of of item in previous row
df['Position'] = df['Signal'].diff()

df['Buy'] = np.where(df['Position']==1, df['Close'], np.NAN)
df['Sell'] = np.where(df['Position']==-1, df['Close'], np.NAN)

# plt.scatter(df['Date'],df['Buy'],label = 'Buy Signal', marker = '^', color="green")
# plt.scatter(df['Date'],df['Sell'],label = 'Sell Signal', marker = 'v', color="red")
   
cleanedSell = pd.notnull(df['Sell'])
cleanedBuy = pd.notnull(df['Buy']) 


cashgain = 0
percentGain = 0

print("   Date           Sold      Bought    Profit")
print("--------------------------------------------")
for (salep, buyp, i) in zip(df[cleanedSell]['Sell'], df[cleanedBuy]['Buy'], df[cleanedSell].index):
    prof = salep-buyp
    perc = prof/buyp
    print(i.strftime("%d-%b-%Y"), "--->", "{:.2f}".format(salep), " - ", "{:.2f}".format(buyp), " = ", "{:.2f}".format(prof))
    cashgain+=prof
    percentGain += perc
    
   
print("\nStrategy profit from 1 share: $", "{:.2f}".format(cashgain))
print("Profit if buy and hold from day 1: $", "{:.2f}".format(df['Close'].iloc[-1] - df['Close'].iloc[0]))


marketGain = (df['Close'].iloc[-1] - df['Close'].iloc[0])/df['Close'].iloc[0]
print("\nGeneral Market % increase: ", "{:.2%}".format(marketGain))
print("Strategy % increase: ", "{:.2%}".format(percentGain))