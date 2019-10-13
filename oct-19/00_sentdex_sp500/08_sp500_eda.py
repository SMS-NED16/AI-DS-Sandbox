"""08_sp500_eda.py - Exploratory data analysis of adjusted closing stock prices 
for the S&P500 stocks from 2000 to the end of 2016. Will contain many missing 
values (due to the nature of the data - not all stocks were traded for the entire duration).
Will try to find some relationships in the data"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style

def visualize_data():
	# Read the CSV with adjusted closing stock prices
	df = pd.read_csv('sp500_joined_closes.csv')

	# Sanity Check - Plotting the price for Apple - AAPL
	style.use('ggplot')
	# df['AAPL'].plot()
	# plt.show()

	# Establishing correlation table for all columns in the dataframe
	df_corr = df.corr()
	print(df_corr.head())

	# Visualizing correlation data
	data = df.corr().values		# get np array of rows and cols sans index/headers
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)	# 1 row, 1 col, first plot in the grid
	
	# Color code high and low correlations according the color map
	heatmap = ax.pcolor(data, cmap=plt.cm.RdYlGn)		

	# Legend for the heatmap
	fig.colorbar(heatmap)

	# Markers along the x and y axes - ticks at every 'half' mark
	ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)	# rows
	ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)	# cols

	# Small gap at the top of the matplotlib graph, we want this to be at the bottom
	# Modifying positioning of the x axis as well
	ax.invert_yaxis()
	ax.xaxis.tick_top()

	# Labels should be identical because its a correlation table
	column_labels = df_corr.columns
	row_labels = df_corr.index
	ax.set_xticklabels(column_labels)	
	ax.set_yticklabels(row_labels)
	plt.xticks(rotation=90)

	# Setting numeric ranges for color: what values do red and green represent?
	heatmap.set_clim(-1, 1)

	plt.tight_layout()
	plt.show()

# Call the function	
visualize_data()