import pandas as pd
import requests
from bs4 import BeautifulSoup

#main/required URLs
gold_url = "https://www.investing.com/commodities/gold-historical-data/"
silver_url = "https://www.investing.com/commodities/silver-historical-data/"


def get_futures_data(url, commodity):
    #executing GET request, and using html parser to scrape table out
    page = requests.get(url, headers = {'User-Agent': 'Custom user agent'})
    text = page.text
    soup = BeautifulSoup(text, 'html.parser')
    table = soup.find( "table", id="curr_table")

    #adding all rows from required table into a list 'rows'
    rows=list()
    for row in table.findAll("tr"):
        rows.append(row.text.splitlines())

    #convert the 'rows' list into dataframe, with proper column headers, and convert all date-times to iso format
    df = pd.DataFrame(rows[1:], columns=rows[0])
    df.dropna(inplace=True)
    df = df[['Date', 'Price', 'Open', 'High', 'Low']]
    df['Date'] = pd.to_datetime(df['Date'])

    #converting all price values to 'float' type, and store into csv with appropriate file name
    df['Price']= df['Price'].apply(lambda x: float(x.replace(',', '')))
    file_name = commodity + '.csv'
    df.to_csv(file_name, columns=['Date', 'Price', 'Open', 'High', 'Low'])

    print (commodity + " file extracted/updated...")    #printing fo clarity when API is fired
    return file_name
