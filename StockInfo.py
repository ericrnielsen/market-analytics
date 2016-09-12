#!/usr/bin/python

# Import everything I need
import os
import re
from yahoo_finance import Share
import collections

class StockInfo:

    def __init__(self, ticker):
        good_ticker = ticker.encode('ascii', 'ignore')
        share = Share(good_ticker)
        self.share = share
        self.price = share.get_price()
        self.change = share.get_change()
        #self.percent_change = share.get_percent_change()
        self.volume = share.get_volume()
        self.prev_close = share.get_prev_close()
        self.open = share.get_open()
        self.avg_daily_volume = share.get_avg_daily_volume()
        self.stock_exchange = share.get_stock_exchange()
        self.market_cap = share.get_market_cap()
        self.book_value = share.get_book_value()
        self.ebitda = share.get_ebitda()
        self.dividend_share = share.get_dividend_share()
        self.dividend_yield = share.get_dividend_yield()
        self.earnings_share = share.get_earnings_share()
        self.days_high = share.get_days_high()
        self.days_low = share.get_days_low()
        self.year_high = share.get_year_high()
        self.year_low = share.get_year_low()
        self.day50_moving_avg = share.get_50day_moving_avg()
        self.day200_moving_avg = share.get_200day_moving_avg()
        self.price_earnings_ratio = share.get_price_earnings_ratio()
        self.earnings_growth_ratio = share.get_price_earnings_growth_ratio()
        self.price_sales = share.get_price_sales()
        self.price_book = share.get_price_book()
        self.short_ratio = share.get_short_ratio()
        self.trade_datetime = share.get_trade_datetime()
        self.name = share.get_info()['symbol']
        #self.name = share.get_name()

    # Still needs to be implemented
    def __str__(self):
        to_return = ''
        sorted_dict = collections.OrderedDict(sorted(self.make_dict().items(), key=lambda t: t[0]))
        for key in sorted_dict:
            to_return += '{0}: {1}\n'.format(key, str(sorted_dict[key]))
        return to_return

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    # Turn the object into a dictionary
    def make_dict(self):
        to_return = {'price' : self.price, \
                     'change' : self.change, \
                     'volume' : self.volume, \
                     'prev_close' : self.prev_close, \
                     'open' : self.open, \
                     'avg_daily_volume' : self.avg_daily_volume, \
                     'stock_exchange' : self.stock_exchange, \
                     'market_cap' : self.market_cap, \
                     'book_value' : self.book_value, \
                     'ebitda' : self.ebitda, \
                     'dividend_share' : self.dividend_share, \
                     'dividend_yield' : self.dividend_yield, \
                     'earnings_share' : self.earnings_share, \
                     'days_high' : self.days_high, \
                     'days_low' : self.days_low, \
                     'year_high' : self.year_high, \
                     'year_low' : self.year_low, \
                     '50day_moving_avg' : self.day50_moving_avg, \
                     '200day_moving_avg' : self.day200_moving_avg, \
                     'price_earnings_ratio' : self.price_earnings_ratio, \
                     'earnings_growth_ratio' : self.earnings_growth_ratio, \
                     'price_sales' : self.price_sales, \
                     'price_book' : self.price_book, \
                     'short_ratio' : self.short_ratio, \
                     'trade_datetime' : self.trade_datetime, \
                     'name' : self.name}
        return to_return
