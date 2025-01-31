# Import all the necessary libraries:
import yfinance as yf

import pandas as pd

import requests

from bs4 import BeautifulSoup

import plotly.graph_objects as go

from plotly.subplots import make_subplots


def make_graph(stock_data, revenue_data, stock):

    # This creates a figure with two rows and one column. Both subplots will share the same x-axis (Date).
    fig = make_subplots(rows = 2, cols = 1, shared_xaxes = True, subplot_titles = ("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)

    # Filter the stock data up to specific date, i.e. 2021-06-14
    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']

    # Filter the revenue data up to specific date, i.e. 2021-04-30
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']

    # A line plot of the stock price in the first subplot, and a line plot of the revenue in the second subplot.

    # Adds a line plot to the figure. The x-axis data is the Date column from stock_data_specific, which is converted to datetime format using pd.to_datetime().
    ## The y-axis data is the Close price from stock_data_specific, converted to float using astype("float").
    ## The name for the trace (line) is "Share Price"
    ## It also specifies that this trace should be placed in the first row, first column
    fig.add_trace(go.Scatter(x = pd.to_datetime(stock_data_specific.Date), y = stock_data_specific.Close.astype("float"), name = "Share Price"), row = 1, col = 1)

    # Adds a line plot to the figure. The x-axis data is the Date column from revenue_data_specific, which is converted to datetime format using pd.to_datetime().
    ## The y-axis data is the Revenue Data from revenue_data_specific, converted to float using astype("float").
    ## The name for the trace (line) is "Revenue"
    ## It also specifies that this trace should be placed in the second row, first column 
    fig.add_trace(go.Scatter(x = pd.to_datetime(revenue_data_specific.Date), y = revenue_data_specific.Revenue.astype("float"), name = "Revenue"), row = 2, col = 1)

    # Title for x-axis is "Date" for both subplots
    fig.update_xaxes(title_text = "Date", row = 1, col = 1)

    fig.update_xaxes(title_text = "Date", row = 2, col = 1)

    # Title for y-axis is "Price ($US)" for first subplot (row = 1, col = 1)
    fig.update_yaxes(title_text = "Price ($US)", row = 1, col = 1)

    # Title for y-axis is "Revenue ($US Millions)" for second subplot (row = 2, col = 1)
    fig.update_yaxes(title_text = "Revenue ($US Millions)", row = 2, col = 1)

    fig.update_layout(showlegend = False, height = 900, title = stock, xaxis_rangeslider_visible = True)

    fig.show()
