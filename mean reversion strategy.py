import pandas as pd
import pandas_datareader as pdr
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['figure.figsize'] = 8,6
import seaborn as sb
import datetime as dt
sb.set()

start = dt.datetime(2015,1,1)
end = dt.datetime(2017,12,20)

df = pd.DataFrame(pdr.get_data_yahoo("BAC", start, end)['Close'])

ma = 21
df['returns'] = np.log(df["Close"]).diff()
df['ma'] = df['Close'].rolling(ma).mean()
df['ratio'] = df['Close'] / df['ma']

percentiles = [3, 5, 10, 50, 90, 95, 97]
p = np.percentile(df['ratio'].dropna(), percentiles)

# df['ratio'].dropna().plot(legend = True)
# plt.axhline(p[0], c= (.5,.5,.5), ls='--')
# plt.axhline(p[2], c= (.5,.5,.5), ls='--')
# plt.axhline(p[-1], c= (.5,.5,.5), ls='--');


# when the ratio goes above 95 percentile I short it because it should go down soon
# when ratio goes below 5th percentile I buy it because it should go up soon
high = p[-1]
low = p[0]
df['position'] = np.where(df.ratio < high, -1, np.nan)
df['position'] = np.where(df.ratio > low, 1, df['position'])
df['position'] = df['position'].ffill()

df['myreturn'] = df['returns'] * df['position'].shift()

# plt.plot(np.exp(df['returns'].dropna()).cumprod(), label='Buy/Hold')
# plt.plot(np.exp(df['myreturn'].dropna()).cumprod(), label='Strategy')

plt.plot(df['Close'].dropna(), label = 'close')
plt.plot(df['ma'].dropna(),label = 'sma')

plt.legend()



print("BUY AND HOLD:   ", np.exp(df['returns'].dropna()).cumprod()[-1] -1)
print("STRATEGY:       ", np.exp(df['myreturn'].dropna()).cumprod()[-1] - 1)
print("\n")