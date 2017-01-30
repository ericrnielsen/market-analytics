#!/usr/bin/python

import re

class Article:

    def __init__(self):
        self.name = ""
        self.href = ""
        self.date = ""
        self.time = ""
        self.tickers = []
        self.keywords = []

    def __str__(self):
        to_return = 'name:    {0}\nhref:    {1}\ndate:    {2}\ntime:    {3}\ntickers: {4}\n'.format( \
        self.name, self.href, self.date, self.time, self.tickers)
        return to_return

    # Set the article name, also automatically sets the ticker values if there are tickers
    def set_name(self, name):
        self.name = name.encode('ascii', 'ignore')
        parse1_tickers = []
        parse1_tickers = re.findall('\((.*?)\)',name)
        for item in parse1_tickers:
            if len(item.split(":")) > 1:
                if not (str(item.split(":")[1]) == "more..."):
                    self.add_ticker(str(item.split(":")[1]))
            else:
                if not (str(item) == "more..."):
                    self.add_ticker(str(item))

    def set_href(self, href):
        self.href = href.encode('ascii', 'ignore')

    def set_date(self, date):
        self.date = date.encode('ascii', 'ignore')

    def set_time(self, time):
        self.time = time.encode('ascii', 'ignore')

    def add_ticker(self, ticker):
        self.tickers.append(ticker)

    def add_keywords(self, keywords):
        self.tickers.append(keywords)

    def __eq__(self, other):
        #return self.__dict__ == other.__dict__
        if (self.name == other.name):
            if (self.date == other.date):
                if (self.time == other.time):
                    if (self.tickers == other.tickers):
                        if (self.keywords == other.keywords):
                            return True
        return False
