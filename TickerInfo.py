#!/usr/bin/python

# Import everything I need
import os
import objc
from yahoo_finance import Share
import datetime

def get_info(ticker):


    today = datetime.datetime.today()

    yahoo = Share(ticker)

    info = yahoo.get_historical('2010-01-01', '2016-09-02')

    n = 1
    max_close = 0
    found = {}
    for item in info:
        if item[Close] > max_close:
            max_close = item[Close]
            found = item


        print '#', n
        n += 1
        for key in item:
            print key, " : ", item[key]
        print ''



'''
Paused here - need to make function to get 52 week high
def get_high52weekclose(historical_data):

    for item in historical_data:
        if item[Date]
'''
