#!/usr/bin/python

# Normal import
import sys, os, inspect, json
import datetime as dt
import pandas as pd
from collections import defaultdict
from io import BytesIO
from flask import Flask, send_file

# Need to get them from the directory above
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
import menu_options
sys.path.insert(0,currentdir)

# Set up flask
#app = Flask(__name__)
#ctx = app.app_context()
#ctx.push()

if __name__ == "__main__":

    testing = False

    ######################################################################################
    # Testing - so specify input data here
    ######################################################################################
    if (testing == True):
        input_data = {}
        input_data['Tickers'] = ['FB', 'MSFT']
        input_data['Start'] = '2016-01-01'
        input_data['End'] = 'today'

    ######################################################################################
    # Get values passed in
    ######################################################################################
    else:
        input_data = {}
        input_data['Tickers'] = sys.argv[3].split(",")
        input_data['Start'] = sys.argv[1]
        input_data['End'] = sys.argv[2]

    #print input_data    

    ######################################################################################
    # Working with the data in the JSON object
    ######################################################################################

    # List of tickers
    tickers = []
    for each in input_data['Tickers']:
        tickers.append(each.encode('ascii', 'ignore'))
    
    # Start date and datetime
    start_date = dt.datetime.strptime(input_data['Start'], '%Y-%m-%d').date()
    start_time = dt.datetime.strptime('00:00:00', '%H:%M:%S').time()
    start_datetime = dt.datetime.combine(start_date, start_time)

    # End date and datetime
    if (input_data['End'].lower() == 'today'):
        end_date = dt.datetime.now().date()
    else:
        end_date = dt.datetime.strptime(input_data['End'], '%Y-%m-%d').date()
    end_time = dt.datetime.strptime('00:00:00', '%H:%M:%S').time()
    end_datetime = dt.datetime.combine(end_date, end_time)

    ######################################################################################
    # Setting global variables
    ######################################################################################
   
    master_tickers = {}
    master_stock_data = defaultdict(list)
    master_ticker_reference = None #pd.read_csv('ticker_reference.csv')


    ######################################################################################
    # Set selections for calling the functions
    ######################################################################################

    selections = {}

    # Quick run type (option 2 is to compute stock data)
    selections['Quickrun'] = 2
    selections['Web App'] = True
    # Tickers
    selections['Tickers'] = tickers

    # Days to search
    selections['Days to Search'] = int((end_date - start_date).days)

    # Start and end dates
    selections['Start'] = start_datetime
    selections['End'] = end_datetime

    #print selections

    ######################################################################################
    # Call functions
    ######################################################################################

    # Add tickers to ticker list
    menu_options.edit_ticker_list(master_tickers, 'quick', selections)

    # Get market data for identified tickers
    menu_options.get_financial_data(master_tickers, master_stock_data, master_ticker_reference, 'quick', selections)

    # Analyze market data (do calculations) for identified tickers
    output = menu_options.compute_stock_metrics(master_stock_data, master_ticker_reference, 'quick', selections)
    print output

    # Construct response
    #output.seek(0)
    #with ctx:
    #    send_file(output, attachment_filename="testing.xlsx", as_attachment=True)

