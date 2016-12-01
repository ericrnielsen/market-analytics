#!/usr/bin/python

import sys
import operator
import time
import datetime
import pandas as pd

#########################################################################
#########################################################################
#########################################################################
# If user wants to determine if a ticker is valid
def check_valid(ticker, master_ticker_reference):
    return ticker in master_ticker_reference['Ticker'].values

#########################################################################
#########################################################################
#########################################################################
# If user wants to get the company name for a ticker
def get_company_name(ticker, master_ticker_reference):
    row = master_ticker_reference.loc[master_ticker_reference['Ticker'] == ticker]
    try:
        company_name = row['Name'].values[0]
    except:
        company_name = ticker
    return company_name

#########################################################################
#########################################################################
#########################################################################
# If user wants to get the sector a ticker
def get_sector(ticker, master_ticker_reference):
    row = master_ticker_reference.loc[master_ticker_reference['Ticker'] == ticker]
    return row['Sector'].values[0]

#########################################################################
#########################################################################
#########################################################################
# If user wants to get the industry a ticker
def get_industry(ticker, master_ticker_reference):
    row = master_ticker_reference.loc[master_ticker_reference['Ticker'] == ticker]
    return row['Industry'].values[0]

#########################################################################
#########################################################################
#########################################################################
# If user wants to get the price a ticker
def get_price(ticker, master_ticker_reference):
    row = master_ticker_reference.loc[master_ticker_reference['Ticker'] == ticker]
    return row['Price'].values[0]

#########################################################################
#########################################################################
#########################################################################
# If user wants to get the colection a ticker
def get_collection(ticker, master_ticker_reference):
    row = master_ticker_reference.loc[master_ticker_reference['Ticker'] == ticker]
    return row['Collection'].values[0]
