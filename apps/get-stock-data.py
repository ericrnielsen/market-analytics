#!/usr/bin/python

# Normal import
import sys, os, inspect, json
import datetime as dt
import pandas as pd
from collections import defaultdict

# Need to get them from the directory above
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
import menu_options
sys.path.insert(0,currentdir)


if __name__ == "__main__":

    testing = True

    ######################################################################################
    # Testing - so specify input data here
    ######################################################################################
    if (testing == True):
        input_dict = {'Tickers':['FB', 'MSFT'], 'Start':'2016-01-01', 'End':'today'}
        input_json = json.dumps(input_dict)
        input_data = json.loads(input_json)

    ######################################################################################
    # Get JSON object passed in
    ######################################################################################
    else:
        try:
            passed_in = sys.argv[1]
            input_data = json.loads(passed_in)
        except:
            print "ERROR: Invalid input!"
            sys.exit(1)

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
    master_ticker_reference = pd.read_csv('../ticker_reference.csv')
    master_stock_data = defaultdict(list)

    ######################################################################################
    # Set selections for calling the functions
    ######################################################################################

    selections = {}

    # Quick run type (option 2 is to compute stock data)
    selections['Quickrun'] = 2

    # Tickers
    selections['Tickers'] = tickers

    # Days to search
    selections['Days to Search'] = int((end_date - start_date).days)

    # Start and end dates
    selections['Start'] = start_datetime
    selections['End'] = end_datetime

    ######################################################################################
    # Call functions
    ######################################################################################

    # Add tickers to ticker list
    menu_options.edit_ticker_list(master_tickers, 'quick', selections)

    # Get market data for identified tickers
    menu_options.get_financial_data(master_tickers, master_stock_data, master_ticker_reference, 'quick', selections)

    # Analyze market data (do calculations) for identified tickers
    menu_options.compute_stock_metrics(master_stock_data, master_ticker_reference, 'quick', selections)


