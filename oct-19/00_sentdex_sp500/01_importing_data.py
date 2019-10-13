"""Importing data for a single stock"""
# Importing required libraries
import datetime as dt 					# send start and end dates for data from reader
import matplotlib.pyplot as plt 		# package that helps us make plots/graphs/charts
from matplotlib import style			# a specific style for matplotlib charts
import pandas as pd 					
import pandas_datareader.data as web	# for actually grabbing data from online finance API

# One of many possible styles available in matplotlib
style.use('ggplot')

# Setting up API call to Morningstar API to get Tesla stock prices from '00 - '16
start = dt.datetime(2000, 1, 1);	# year/month/day
end = dt.datetime(2016, 12, 31);	# year/month/day


# DataReader returns a pandas dataframe with stock price data for the stock's ticker for specified dates
# In this case, a request is sent Tesla ticker (TSLA) to the `yahoo` finance API endpoint
# Which returns a dataframe of prices for this stock between the start and end dates
df = web.DataReader('TSLA', 'yahoo', start, end)

# Examine the first few rows in the dataset for an overview
print(df.head())

# Examine the last few rows in the dataset
print(df.tail())

"""Data returned - opening price, highest price, lowest price, closing price, volume (total shares traded)
and adjusted closing price (price adjusted for stocks being split)"""

# df.reset_index(inplace=True)
# df.set_index("Date", inplace=True)
# df = df.drop("Symbol", axis=1)

# print(df.head())
