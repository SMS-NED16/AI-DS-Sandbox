"""Demonstrates different ways in which we can read data into a dataframe"""

# Libraries are still the same
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

# Using ggplot's color scheme for plot
style.use('ggplot')

# Start and end dates for stock prices
start = dt.datetime(2000, 1, 1)
end = dt.datetime(2016, 12, 31)

# METHOD 1 - Reading data from the web via an API call
# commented out b/c stored in CSV after first run
# df = web.DataReader('TSLA', 'yahoo', start, end) 

# Check that the data was read successfully
# print(df.tail(6))

# Can save data from a dataframe to a CSV - comma-separated value file
# df.to_csv('tesla.csv')


# METHOD 2 - Reading data from a CSV on local storage instead of from API call
# Normally, when we read in a CSV file, we need to specify which col is index
df = pd.read_csv('tesla.csv')
print(df.head())	# This has an index colum - 0, 1, 2, 3, 4,...

# If we want to use the dates as the index, can specify this when reading from the CSV
# In this case, we're telling pandas to treat possible date strings as datetime objs
# and to treat the first colum (0th column in csv) as the index_col - in this case the date
df = pd.read_csv('tesla.csv', parse_dates=True, index_col=0)
print("After parsing the CSV with instructions to parse dates and treat index_col as 0")
print(df.head())

"""Can read from CSV, JSON, DB like SQL, and lots of other sources"""

# Plotting data using `pandas` - implicitly calls matplotlib on the backend
df.plot()
plt.show()		# not necessary in interactive Python dev envs

# Specifying which columns of the dataframe we want to display
df['Adj Close'].plot()
plt.show()

# Can also plot multiple columns at the same time
df[['Open', 'High']].plot()
plt.show()
