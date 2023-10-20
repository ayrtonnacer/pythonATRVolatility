# pythonforfinance.substack.com

# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import yfinance as yf

# Define the function to obtain historical data for an asset
def get_data(ticker, start, end):
    data = yf.download(ticker, start, end)
    data = data[['Open', 'High', 'Low', 'Close']].copy()
    return data

# Call the function and store the data in a variable
data = get_data('AAPL', '2023-01-01', '2023-10-18')

# Define the function to calculate the true range
def true_range(data):
    data.loc[:, 'previous_close'] = data['Close'].shift(1)
    data.loc[:, 'high-low'] = data['High'] - data['Low']
    data.loc[:, 'high-pc'] = abs(data['High'] - data['previous_close'])
    data.loc[:, 'low-pc'] = abs(data['Low'] - data['previous_close'])
    tr = data[['high-low', 'high-pc', 'low-pc']].max(axis=1)
    return tr

# Call the function and store the true range in a new column in the dataframe
data.loc[:, 'TR'] = true_range(data)

# Define the function to calculate the moving average of the true range
def atr(data, period):
    atr = data['TR'].rolling(period).mean()
    return atr

# Call the function and store the moving average in a new column in the dataframe
data.loc[:, 'ATR'] = atr(data, 14)

# Define the function to plot the data
def plot_data(data, ticker):
    fig, ax = plt.subplots(2, 1, sharex=True)

    # Format the x-axis labels
    ax[1].xaxis.set_major_locator(mdates.MonthLocator()) 
    ax[1].xaxis.set_minor_locator(mdates.WeekdayLocator())  
    ax[1].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  
    ax[0].plot(data['Close'], label='Closing Price', color= '#c91414')
    ax[0].set_title(f'Price and Volatility of {ticker}')
    ax[0].set_ylabel('Price')
    ax[0].legend()

    ax[1].plot(data['ATR'], label='ATR (14 days)', color='#fcbd0b')
    ax[1].set_xlabel('Date')
    ax[1].set_ylabel('ATR')
    ax[1].legend()

    fig.autofmt_xdate()  

    plt.show()

# Call the function and display the chart
plot_data(data, 'AAPL')

