"""More about data manipulation and candlestick graphs. First, we sample the
opening, closing. high, and low price for the stock at every 10 days and feed it into
a new dataframe with custom dates. We then plot a candlestick graph, which requires converting
datetime dates to matplotlib dates."""

# Boilerplate
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')

# New libaries - candlestick graphs and matplotlib's own date objs
from mpl_finance import candlestick_ohlc 
import matplotlib.dates as mdates 

# Read data
df = pd.read_csv('tesla.csv', parse_dates=True, index_col=0)

# Create 100 days moving average price column
df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()
print(df.head())

"""Resample data at longer intervals (e.g. 1 day data sampled at 10 day intervals)"""
# 10D - Resample dataset to create the mean stock price at every 10 days
# OHLC - Open, high, low, close
df_ohlc = df['Adj Close'].resample('10D').ohlc() # use adjusted closing price to calc these vals
df_volume = df['Volume'].resample('10D').sum()	# True volume over 10 days

# Check the dataset was created successfully
print("OHLC\n", df_ohlc.head())
print("Volume\n", df_volume.head())

"""Candlestick Graph - wants not just OHLC prices, but also wants dates in a specific format"""
df_ohlc.reset_index(inplace=True)	# Date is now the first column
print(df_ohlc.head())				# Verify

# Convert the datetime dates matplotlib dates - converts datetime obj to mdate
df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num) 
print(df_ohlc.head())

# Generating subplots in a grid
ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)

# Function that will display matplotlib date as human readable datetime date
ax1.xaxis_date()

# Configure the candlestick graph for the OHLC prices and attach to axis 1
candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g') # Color up -> color to indicate rise

# Configure the second axis - x axis, upper bound, lower bound for fill
ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)

# Should show a plot
plt.show()