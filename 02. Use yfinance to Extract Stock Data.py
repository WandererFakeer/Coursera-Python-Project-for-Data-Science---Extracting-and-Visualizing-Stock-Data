# Using the Ticker function enter the ticker symbol of the stock we want to extract data on to create a ticker object. The stock is Tesla and its ticker symbol is TSLA.
tesla = yf.Ticker("TSLA")

# Using the ticker object and the function history extract stock information and save it in a dataframe named tesla_data. Set the period parameter to "max".
tesla_data = tesla.history(period = "max")

# Reset the index using the reset_index(inplace=True) function on the tesla_data DataFrame and display the first five rows of the tesla_data dataframe using the head function.
tesla_data.reset_index(inplace = True)

tesla_data.head()
