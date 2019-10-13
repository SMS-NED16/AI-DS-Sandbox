"""After reading and saving stock data for all SP500 stocks into separate CSVs,
we're going to combine them into a single pandas dataframe."""
import pandas as pd
import os 
import datetime as dt

def compile_data():
	# First create a list of tickers already in memory. Doing this because not all tickers
	# in the pickle file will have data downloaded.

	# First store a list of all tickers whose CSV files are stored in the directory
	cwd = str(os.getcwd())
	stock_dfs_dir = os.path.join(cwd, 'stock_dfs/')
	csv_files = os.listdir(stock_dfs_dir)
	tickers = [name.split('.csv')[0] for name in csv_files]

	# Instantiate a DataFrame to hold closing stock prices for all tickers on each date 
	main_df = pd.DataFrame()

	# For every ticker in the list of tickers
	for count, ticker in enumerate(tickers):
		# Create a new dataset by reading from the appropriate file
		df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))

		# Date is the index column
		df.set_index('Date', inplace=True)

		# Change the name of the 'Adj Close' column to the ticker
		df.rename(columns={'Adj Close': ticker}, inplace=True)

		# Drop all columns except the one with the ticker's name (i.e. Adj Close)
		df.drop(['Open', 'High', 'Low', 'Close', 'Volume'], axis=1, inplace=True)

		# Append the data frame to the main dataframe
		if main_df.empty:
			main_df = df
		else:
			main_df = main_df.join(df, how='outer')	# OUTER JOIN - won't lose data in case of incompatible cols

		# When reading the CSVs, update user after reading every 10 files
		if count % 10 == 0:
			print(count) 	

	# Sanity check
	print(main_df.head())

	# Save the main dataframe to a separate CSV so we don't have to read/combine separately
	main_df.to_csv('sp500_joined_closes.csv')

# Call the function - some companies will have NaN for Adjusted Closing price - possibly because
# they weren't trading on that date, or weren't even founded.
compile_data()