import numpy as np
import pandas as pd
from flask import Flask, Response, request, url_for
import json


import fetch    #importing 'fetch' file

api = Flask(__name__)   #create flask application object

# executes a GET request, scrapes for the table data, and stores into CSV in relative project directory -- also, updates it
GOLD_FILE = fetch.get_futures_data(fetch.gold_url, 'gold')
SILVER_FILE = fetch.get_futures_data(fetch.silver_url, 'silver')


@api.route('/commodity/<start_date>/<end_date>/<commodity_type>')   #defining the endpoint, with required parameters - brute
#@api.route('/commodity?start_date=<start_dt>&end_date=<end_dt>&commodity_type=<commodity>')    #defining the endpoint, with required parameters - query string

def get_data(start_date, end_date, commodity_type):

    #handling the input commodity type
    if commodity_type.startswith('gold'):
        file_name  = GOLD_FILE
    elif commodity_type.startswith('silver'):
        file_name = SILVER_FILE
    else:
        return Response('Invalid Commodity', status=400)    #error response


    df = pd.read_csv(file_name) #reading the CSV file as a pandas dataframe
    df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]  #splicing the dataframe to contain only the dates requested
    prices = df['Price']    #contains a set (type) of all prices for the requested dates


    #required response-payload structure
    payload = {
        'data':{
            date:price for date, price in zip(df['Date'], df['Price'])  #listing out all dates requested, with their corresponding prices
        },
        'mean': np.mean(prices),
        'variance' : np.var(prices)
    }
    payload = json.dumps(payload)

    return Response(payload, status=200, content_type='application/json')


#main call
if __name__ == "__main__":
    api.run('127.0.0.1', port=8080, debug=True)