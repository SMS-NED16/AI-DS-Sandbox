"""S&P 500 is a list of the top 500 companies in the market by market capitalization.
Market capitalization is a measure of the value of the company since cap = share_price * 
outstanding_shares. So this index is a summary of thr 5000 most valuable companies in the market"""

# Will use beatuifulsoup4 to create list of S&P500 companies tickers by scraping Wikipedia
import bs4 as bs 	# Python webscraping library
import pickle		# Serializes any Python object and save it
import requests		# For making HTTP request with Python

# For getting and storing stock data for all companies in ticker list
import os
import pandas as pd
import pandas_datareader.data as web
import requests
import datetime as dt

def save_sp500_tickers():
	"""Makes an HTTP request to Wikipedia page for S&P 500 and uses beautifulsoup4
	to parse its contents and create a table of tickers."""
	REQ_URL = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

	# Make a request to the URL and store its response
	resp = requests.get(REQ_URL)

	# Create BS4 object from text of source code. `lxml` is parser option
	soup = bs.BeautifulSoup(resp.text, 'lxml')

	# Find the table with the S&P500 data using the table class
	table = soup.find('table', {'class': 'wikitable sortable'})

	# Empty list that will store the tickers from the table
	tickers = []

	# For each row in the table (excluding the header)
	for row in table.findAll('tr')[1:]:
		# Append the first column of each row as text to the tickers list
		ticker = row.findAll('td')[0].text 

		# Before appending, remove escape chars
		ticker = ticker.replace('\n', '')

		# Then append this to the list of tickers
		tickers.append(ticker)

	# Once all tickers read, write bytes to a pickle file
	with open("sp500tickers.pickle", "wb") as f:
		pickle.dump(tickers, f)	

	# Return the list of tickers so that it can be read w/o web scraping later
	return tickers

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
		if not os.path.exists('stock_dfs/{}.csv'.format(ticker.replace('.', '-'))):
			# Try-except 
			try: 
				print("Downloading data for ", ticker.replace('.', '-'))
				df = web.DataReader(ticker, 'yahoo', start, end)
			except Exception:
				print("Could not get data for ", ticker)
			else:
				df.to_csv('stock_dfs/{}.csv'.format(ticker.replace('.', '-')))
		else:
			print("Already have {}".format(ticker))


# Getting data for all stocks - this can take a while
get_data_from_yahoo()