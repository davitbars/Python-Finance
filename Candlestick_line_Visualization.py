import datetime as dt
import pandas as pd
import pandas_datareader.data as web 
import matplotlib.pyplot as plt
import mplfinance as mpf
from matplotlib import style

style.use('ggplot')

start = dt.datetime(2017,1,1)
end = dt.datetime(2021,4,1)
df = web.DataReader('TSLA', 'yahoo', start, end)

df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()
df.dropna(inplace=True)

df_ohlc = df['Adj Close'].resample('10D').ohlc()
df_ohlc.columns = ['Open', 'High', 'Low', 'Close']
df_volume = df['100ma'].resample('10D').mean()

mpf.plot(df_ohlc, type='candle', style='charles', title='10 Days', ylabel='  ', ylabel_lower='  ', figratio=(25,10), figscale=1, mav=50, volume=False)

ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
#ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)

ax1.plot(df.index, df['Adj Close'], label="Adjusted Close")
ax1.plot(df.index, df['100ma'], label="100 day Average")

plt.legend()
plt.show()
