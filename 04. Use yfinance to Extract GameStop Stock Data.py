# Using the Ticker function enter the ticker symbol of the stock we want to extract data on to create a ticker object. The stock is GameStop and its ticker symbol is GME.
gamestop = yf.Ticker("GME")

# Using the ticker object and the function history extract stock information and save it in a dataframe named gme_data, setting the period parameter to "max".
gme_data = gamestop.history(period = "max")

# Reset the index using the reset_index(inplace=True) function on the gme_data DataFrame and display the first five rows of the gme_data dataframe using the head function.
gme_data.reset_index(inplace = True)

gme_data.head()
