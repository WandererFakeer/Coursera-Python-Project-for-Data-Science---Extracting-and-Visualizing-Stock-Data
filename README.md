# Extracting and Visualizing Tesla and GameStop Stock Data
Here I will extract 2 stock data, `Tesla` and `GameStop` and then will display their respective data in graph.

## Import all the necessary libraries:

``` 
import yfinance as yf

import pandas as pd

import requests

from bs4 import BeautifulSoup

import plotly.graph_objects as go

from plotly.subplots import make_subplots
```

## Define Graphing Function
### This function `make_graph()` takes 3 parameters - `stock_data`, `revenue_data`, `stock`, i.e. a dataframe with stock data (Contain `Date` and `Close` columns), a dataframe with revenue data (Contain `Date` and `Revenue` columns), and the name of the stock. 
### It graphs the data of the stock provided in it as arguments. 
### The graph will show data upto June 2021.

```
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
    fig.add_trace(go.Scatter(x = pd.to_datetime(stock_data_specific.Date, infer_datetime_format = True), y = stock_data_specific.Close.astype("float"), name = "Share Price"), row = 1, col = 1)

    # Adds a line plot to the figure. The x-axis data is the Date column from revenue_data_specific, which is converted to datetime format using pd.to_datetime().
    ## The y-axis data is the Revenue Data from revenue_data_specific, converted to float using astype("float").
    ## The name for the trace (line) is "Revenue"
    ## It also specifies that this trace should be placed in the second row, first column 
    fig.add_trace(go.Scatter(x = pd.to_datetime(revenue_data_specific.Date, infer_datetime_format = True), y = revenue_data_specific.Revenue.astype("float"), name = "Revenue"), row = 2, col = 1)

    # Title for x-axis is "Date" for both subplots
    fig.update_xaxes(title_text = "Date", row = 1, col = 1)

    fig.update_xaxes(title_text = "Date", row = 2, col = 1)

    # Title for y-axis is "Price ($US)" for first subplot (row = 1, col = 1)
    fig.update_yaxes(title_text = "Price ($US)", row = 1, col = 1)

    # Title for y-axis is "Revenue ($US Millions)" for second subplot (row = 2, col = 1)
    fig.update_yaxes(title_text = "Revenue ($US Millions)", row = 2, col = 1)

    fig.update_layout(showlegend = False, height = 900, title = stock, xaxis_rangeslider_visible = True)

    fig.show()
```

## 01. Question 1: Use yfinance to Extract Stock Data

### (I). Using the `Ticker` function enter the ticker symbol of the stock we want to extract data on to create a ticker object. The stock is Tesla and its ticker symbol is `TSLA`.
```
tesla = yf.Ticker("TSLA")
```

### (II). Using the ticker object and the function `history` extract stock information and save it in a dataframe named `tesla_data`. Set the period parameter to `"max"`.

```
tesla_data = tesla.history(period = "max")
```

### (III). Reset the index using the `reset_index(inplace=True)` function on the `tesla_data` DataFrame and display the first five rows of the `tesla_data` dataframe using the `head` function.
```
tesla_data.reset_index(inplace = True)

tesla_data.head()
```

![Question 1](https://github.com/user-attachments/assets/7abf612f-171c-43fa-8e14-d7f5ff6a9499)


## 02. Question 2: Use Webscraping to Extract Tesla Revenue Data

### (I). Use the `requests` library to download the webpage: [https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm). Save the text of the response as a variable named `html_data`.

```
html_data = requests.get("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm").text
```

### (II). Parse the html data using `beautiful_soup` using parser i.e `html5lib` or `html.parser`.

```
beautiful_soup = BeautifulSoup(html_data, "html5lib")
```

### (III). Using `BeautifulSoup` or the `read_html` function extract the table with Tesla Revenue and store it into a dataframe named `tesla_revenue`. The dataframe should have columns `Date` and `Revenue`.

#### Using `BeautifulSoup`
```
# Create empty Dataframe with columns "Date" and "Revenue"
tesla_revenue = pd.DataFrame(columns = ["Date", "Revenue"])

# Use the beautiful_soup object to find all the "table" tags
for row in beautiful_soup.find_all("table"):

    # Find the string - "Tesla Quarterly Revenue(Millions of US $)" to get the appropriate Table
    if "Tesla Quarterly Revenue(Millions of US $)" in row.text:

        # Find all the "td" tags, and add the text version of them in the list "date_and_revenue_data", with list comprehension
        date_and_revenue_data = [each_data.text.strip() for each_data in row.find_all("td")]

        # Create a new Dataframe "date_and_revenue_dataframe" with List comprehension, where even index is for "Date" and odd index is for Revenue, with 2 steps. It also adds column     
         # names as "Date" and "Revenue"
        date_and_revenue_dataframe = pd.DataFrame([(date_and_revenue_data[idx], date_and_revenue_data[idx + 1]) for idx in range(0, len(date_and_revenue_data), 2)], columns = ["Date", "Revenue"])

        # Concats this newly created Dataframe "date_and_revenue_dataframe" with previously created empty Dataframe "tesla_revenue"
        tesla_revenue = pd.concat([tesla_revenue, date_and_revenue], ignore_index = True)

```
#### Using `read_html`

```
tesla_revenue = pd.read_html("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm")[1]

tesla_revenue.columns = ["Date", "Revenue"]
```

### (IV). Remove the comma and dollar sign from the `Revenue` column, and remove an null or empty strings in the `Revenue` column.

```
tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(r',|\$',"", regex = True)

tesla_revenue.dropna(inplace=True)

tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]
```

### (V). Display the last 5 row of the `tesla_revenue` dataframe using the `tail` function.

```
tesla_revenue.tail()
```


![Question 2](https://github.com/user-attachments/assets/1b01a9ae-d811-4c6d-8504-2c7df122bd3a)


## 03. Question 3: Use yfinance to Extract Stock Data

### (I). Using the `Ticker` function enter the ticker symbol of the stock we want to extract data on to create a ticker object. The stock is GameStop and its ticker symbol is `GME`.

```
gamestop = yf.Ticker("GME")
```

### (II). Using the ticker object and the function history extract stock information and save it in a dataframe named `gme_data`, setting the period parameter to `"max"`.

```
gme_data = gamestop.history(period = "max")
```

### (III). Reset the index using the `reset_index(inplace=True)` function on the gme_data DataFrame and display the first five rows of the `gme_data` dataframe using the `head` function.

```
gme_data.reset_index(inplace = True)

gme_data.head()
```

![Question 3](https://github.com/user-attachments/assets/3a277572-82d5-47e8-bb71-3e9a73b41720)


## 04. Question 4: Use Webscraping to Extract GME Revenue Data

### (I). Use the `requests` library to download the webpage: [https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html). Save the text of the response as a variable named `html_data_2`.

```
html_data_2 = requests.get("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html").text
```

### (II). Parse the html data using `beautiful_soup` using parser i.e `html5lib` or `html.parser`.

```
beautiful_soup_2 = BeautifulSoup(html_data_2, "html5lib")
```

### (III). Using `BeautifulSoup` or the `read_html` function extract the table with GameStop Revenue and store it into a dataframe named `gme_revenue`. The dataframe should have columns `Date` and `Revenue`.

#### Using `BeautifulSoup`
```
# Create empty Dataframe with columns "Date" and "Revenue"
gme_revenue = pd.DataFrame(columns = ["Date", "Revenue"])

# Use the beautiful_soup object to find all the "table" tags
for row in beautiful_soup_2.find_all("table"):

    # Find the string - "GameStop Quarterly Revenue(Millions of US $)" to get the appropriate Table
    if "GameStop Quarterly Revenue(Millions of US $)" in row.text:

        # Find all the "td" tags, and add the text version of them in the list "date_and_revenue_data", with list comprehension
        date_and_revenue_data = [each_data.text.strip() for each_data in row.find_all("td")]

        # Create a new Dataframe "date_and_revenue_dataframe" with List comprehension, where even index is for "Date" and odd index is for Revenue, with 2 steps. It also adds column     
         # names as "Date" and "Revenue"
        date_and_revenue_dataframe = pd.DataFrame([(date_and_revenue_data[idx], date_and_revenue_data[idx + 1]) for idx in range(0, len(date_and_revenue_data), 2)], columns = ["Date", "Revenue"])

        # Concats this newly created Dataframe "date_and_revenue_dataframe" with previously created empty Dataframe "gme_revenue"
        gme_revenue = pd.concat([gme_revenue, date_and_revenue_dataframe], ignore_index = True)

```

#### Using `read_html`
```
gme_revenue = pd.read_html("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html")[1]

gme_revenue.columns = ["Date", "Revenue"]
```

### (IV). Remove the comma and dollar sign from the `Revenue` column.

```
gme_revenue["Revenue"] = gme_revenue["Revenue"].str.replace(r",|\$", "", regex = True)
```

### (V). Display the last 5 row of the `gme_revenue` dataframe using the `tail` function.

```
gme_revenue.tail()
```

![Question 4](https://github.com/user-attachments/assets/656894d6-cbfa-4049-b45a-08c5e4c3c150)


## 05. Question 5: Plot Tesla Stock Graph

### Use the `make_graph` function, with `tesla_data`, `tesla_revenue` , string - `"Tesla's Historical Share Price and Historical Revenue (Till June 2021)"` as parameters, to graph the Tesla Stock Data. Provide a title for the graph. (Name - **Tesla's Historical Share Price and Historical Revenue (Till June 2021)**)

```
make_graph(tesla_data, tesla_revenue, "Tesla's Historical Share Price and Historical Revenue (Till June 2021)")
```

![Question 5](https://github.com/user-attachments/assets/dd974762-b2ff-42b6-b38d-eca81b1b108e)


## 06. Question 6: Plot GameStop Stock Graph

### Use the `make_graph` function, with `gme_data`, `gme_revenue` , string - `"GameStop's Historical Share Price and Historical Revenue (Till June 2021)"` as parameters, to graph the Tesla Stock Data. Provide a title for the graph. (Name - **GameStop's Historical Share Price and Historical Revenue (Till June 2021)**)

```
make_graph(gme_data, gme_revenue, "GameStop's Historical Share Price and Historical Revenue (Till June 2021)")
```

![Question 6](https://github.com/user-attachments/assets/238eab86-586e-47b4-96ad-91392257e95b)
