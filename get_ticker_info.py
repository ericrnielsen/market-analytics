#!/usr/bin/python

import sys
import operator
import time
import datetime
from Article import Article
from Article_List import Article_List
import tickers
import zergwatch
import streetupdates
import newsoracle
import smarteranalyst
import streetinsider
#import aomarkets
#import marketwatch
#import investorplace
import dominate
from dominate.tags import *
import glob2
import pandas_datareader.data as web
import logging

#########################################################################
#########################################################################
#########################################################################
# If user wants to get current info for a ticker
def get_current(ticker):
    # Suppress logging messages
    logging.getLogger("requests").setLevel(logging.WARNING)
    # Call the function
    stock_info = web.get_quote_yahoo(ticker)
    return stock_info

#########################################################################
#########################################################################
#########################################################################
# If user wants to get historical info for a ticker
def get_historical(ticker, start_date, end_date):
    # Suppress logging messages
    logging.getLogger("requests").setLevel(logging.WARNING)
    # Change start_date to correct format
    start_year = int(float(start_date.split('-')[0]))
    start_month = int(float(start_date.split('-')[1]))
    start_day = int(float(start_date.split('-')[2]))
    start = datetime.datetime(start_year, start_month, start_day)
    # Change end_date to correct format
    end_year = int(float(end_date.split('-')[0]))
    end_month = int(float(end_date.split('-')[1]))
    end_day = int(float(end_date.split('-')[2]))
    end = datetime.datetime(end_year, end_month, end_day)
    # Call the function
    stock_info = web.DataReader(ticker, 'yahoo', start, end)
    return stock_info

#########################################################################
#########################################################################
#########################################################################
# Printing out info about identified top tickers
def print_info(ticker, stock_info):
    print '\n-----------------------------'
    print 'Stock info for {0}'.format(ticker)
    print '-----------------------------'
    print stock_info
