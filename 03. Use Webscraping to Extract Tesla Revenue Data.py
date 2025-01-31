# Use the requests library to download the webpage: https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm. 
 # Save the text of the response as a variable named html_data.

html_data = requests.get("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm").text

# Parse the html data using beautiful_soup using parser i.e html5lib or html.parser.
beautiful_soup = BeautifulSoup(html_data, "html5lib")

# Using BeautifulSoup or the read_html function extract the table with Tesla Revenue and store it into a dataframe named tesla_revenue. The dataframe should have columns Date and Revenue.
 # (I). Using BeautifulSoup

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


 # Or, (II). Using read_html
tesla_revenue = pd.read_html("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm")[1]

tesla_revenue.columns = ["Date", "Revenue"]

# Remove the comma and dollar sign from the Revenue column, and remove an null or empty strings in the Revenue column.
tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(r',|\$',"", regex = True)

tesla_revenue.dropna(inplace=True)

tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

# Display the last 5 row of the tesla_revenue dataframe using the tail function.
tesla_revenue.tail()
