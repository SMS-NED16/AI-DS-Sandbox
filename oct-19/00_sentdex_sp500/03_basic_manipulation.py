"""Basics of manipulating and visualizing stock data"""

import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
style.use('ggplot')

# Read in the stock data from the CSV
df = pd.read_csv('tesla.csv', parse_dates=True, index_col=0)

# Creating a new column to store the result of applying a function to an existing column
# 100ma - 100 moving average: average of the last 100 values - smooths out price over time
# Can use this moving average to filter out noise and assess uptrend/downtrends
df['100ma'] = df['Adj Close'].rolling(window=100).mean()
print(df.head())	# NaN for the first 100 values - can't compute avg if 100 prev vals unavailable
print(df.tail())

# Could drop the columns that contain NaN values (missing values)
df.dropna(inplace=True)	# Don't have to redefine df, can just modify existing df
print(df.head())		# Now rows with missing moving avg values have been removed - lost ~100 days

# A better solution - use `min_periods = 0`. This is the minimum number of observations
# in the window required for value computation
df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()
print(df.head())	# Now no NaN. For first 100, mean = adjusted close price

# Graphing stock prices with pure matplotlib 
# Each matplotlib plot is a figure, and can have multiple subfigures/subplots on axes
# Subplot grid size (rows, cols)-starting point for graph-how many rows the subplot takes
# colspan - how many cols in the grid it takes
ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)			

# Same syntax, only 1 row and 1 column, but x axis will pan/move with that of axis 1
ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1) 

# Make plots by adding data to specific axes - adj close and 100ma on one plot
ax1.plot(df.index, df['Adj Close']);
ax1.plot(df.index, df['100ma']);

# Bar plot of the volume of shares traded on the second subplot.
ax2.bar(df.index, df['Volume'])

# Don't forget to actually render plots
plt.show()