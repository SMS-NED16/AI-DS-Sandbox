def get_data_from_yahoo(reload_sp500=False):
	"""Uses a list of SP 500 tickers to get opening, closing, high, low, adjusted close and volume
	stock data from Yahoo API and stores all stock data in individual directories"""

	# If the user has requested to reload list of tickers, scrape Wikipedia. Otherwise,
	# Read bytes from the list of tickers from the local pickle file
	if reload_sp500:
		tickers = save_sp500_tickers()
	else:
		with open("sp500tickers.pickle", "rb") as f:
			tickers = pickle.load(f)

	# If local copy of the stock data frames doesn't already exist
	if not os.path.exists('stock_dfs'):
		os.makedirs('stock_dfs')

	# Start and end times for the stock data
	start = dt.datetime(2000, 1, 1,)
	end = dt.datetime(2016, 12, 31)

	# Make a separate CSV for every ticker 
	for ticker in tickers:
		# If a CSV file for the current stock doesn't exist
		if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
			# Try-except 
			try: 
				print("Downloading data for ", ticker)
				df = web.DataReader(ticker, 'yahoo', start, end)
			except Exception:
				print("Could not get data for ", ticker)
			else:
				df.to_csv('stock_dfs/{}.csv'.format(ticker))
		else:
			print("Already have {}".format(ticker))
