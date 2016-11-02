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

        # Actual data
        logging.getLogger("requests").setLevel(logging.WARNING)
        self.data = web.DataReader(ticker, 'yahoo', start_date, end_date)

        # Data type (either base or computed)
        self.data_type = 'base'

        # Start date of info (if historical)
        self.start_date = start_date

        # End date of info (if historical)
        self.end_date = end_date

    # Update the data
    def add_metrics(self, df_data):
        self.data = df_data
        self.data_type = 'computed'

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
