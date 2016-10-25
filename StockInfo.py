#!/usr/bin/python

import sys
import operator
import time
import datetime
import pandas_datareader.data as web
import logging

#########################################################################
#########################################################################
#########################################################################
class StockInfo:

    # Init the object
    def __init__(self, ticker, start_date, end_date):
        # Ticker name
        self.ticker = ticker
        # Actual info
        logging.getLogger("requests").setLevel(logging.WARNING)
        self.data = web.DataReader(ticker, 'yahoo', start_date, end_date)
        # Start date of info (if historical)
        self.start_date = start_date
        # End date of info (if historical)
        self.end_date = end_date

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
