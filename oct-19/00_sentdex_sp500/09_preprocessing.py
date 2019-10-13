from collections import Counter

import numpy as np
import pandas as pd


def process_data_for_labels(ticker):
	"""Creates columns showing percentage changes in stock price of `ticker` for `hm_days`"""
	# How many days into the future will we examine for pct changes
	hm_days = 7

	# Reading all the adjsuted closing prices from our dataset
	df = pd.read_csv('sp500_joined_closes.csv', index_col=0)

	# Tickers is the list of stock identifiers
	tickers = df.columns.values.tolist()

	# Start at day 0, look at pct changes in prices from days 1 - 7
	for i in range(1, hm_days + 1):
		# Pct change at the ith day: (value at ith day - value today) / value today
		# Create a new column the pct change at each future day on that date for that stock
		# Shifting done to get future rows (think of it as an upward shift of the column)
		df['{}_{}d'.format(ticker, i)] = (df[ticker].shift(-i) - df[ticker]) / df[ticker] 

	# In case any NaNs, replace with 0
	df.fillna(0, inplace=True)

	# Return the list of tickers and the dataframe with percentage changes on each day for the stock
	return tickers, df

# This will create 7 new columns that show pct change in value of Exxon Mobil stock at each date (row)
tickers, df = process_data_for_labels('XOM')
print(df.head())

def buy_sell_or_hold(*args):		# lets us pass any number of params - in this case, pct change cols for a single date
	"""Uses pct changes to encode decision to buy, sell, or hold specific stock on a specific day"""
	cols = [c for c in args]		# Extracts all future pct changes by row 
	requirement = 0.02				# Threshold used for buy/sell - 2			
	for col in cols:
		if col > requirement:		# If even one column shows 2%+ increase, return 1 - buy before price increases further
			return 1
		if col < -requirement:		# If even one column shows 2%- decrease, return -1 - sell before price decreases further
			return -1

	# No significant increase or decrease
	return 0

# Now map the buy_sell_hold function to each row in the dataset 
def extract_features(ticker):

	# First, get a list of tickers and a dataframe with pct changes for a specific ticker
	tickers, df = process_data_for_labels(ticker)

	# Create label column for each date by mapping buy_sell_hold to each row/date based on future XOM changes
	# The arguments passed to map are the pct changes for the ticker on each date
	df['{}_target'.format(ticker)] = list(map(buy_sell_or_hold, 	# function
		df['{}_1d'.format(ticker)],									# columns for pct changes in stock prices on future days
		df['{}_2d'.format(ticker)],
		df['{}_3d'.format(ticker)],
		df['{}_4d'.format(ticker)],
		df['{}_5d'.format(ticker)],
		df['{}_6d'.format(ticker)],
		df['{}_7d'.format(ticker)]
	))

	# Extract the buy/sell/hold label for each date from the right column
	buy_sell_hold_flags = df['{}_target'.format(ticker)].values.tolist()

	# Sanity check - verify numbers of buy/sell/hold flags in the labels using Collection (needs strings)
	print('Data Spread: ', Counter([str(i) for i in buy_sell_hold_flags]))

	"""Why is the distribution important? 3 classes, so naive assumption: 33% b/w all classes. This is not likely
	 to be the case with our threshold value. We need to tweak the threshold/requirement so that we get a roughly
	 random 33% spread between all classes.
	
	This helps us establish a random baseline: the accuracy that our model would get if it just predicted buy 
	for all examples (no learning was done)
	 """
	df.fillna(0, inplace=True)					# Deal with missing values or NaNs
	df.replace([np.inf, -np.inf], np.nan)		# Division by 0 leads to inf/-inf e.g. pct change from 0 to non-zero val
	df.dropna(inplace=True)						# We can no drop rows with the inf/-inf values as well

	# Extract prices of all stocks from the original dataset, and convert them to pct changes
	df_vals = df[[ticker for ticker in tickers]].pct_change()
	df_vals.replace([np.inf, -np.inf], 0)
	df_vals.fillna(0, inplace=True)

	# Once all prices normalized as pct changes and missing values dealt with, extract features and labels
	X = df_vals.values
	y = df[['{}_target'.format(ticker)]].values

	# Return the featureset, labels, and the original dataframe
	return X, y, df

X, y, df = extract_features('XOM')
print("FEATURES X", X)
print("LABELS y", y)