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
import json
import web
import xml.etree.ElementTree as ET
#import aomarkets
#import marketwatch
#import investorplace
import dominate
from dominate.tags import *
import glob2
from StockInfo import StockInfo 
import menu_options
import menu_optionsAPI
from collections import defaultdict
import pandas as pd
import ticker_reference
#from flask import Flask, request, render_template, jsonify
#from flask.ext.jsonpify import jsonify

if __name__ == "__main__":

    # Variable that allows the code to loop until the user chooses to exit
    continue_code = True

    #########################################################################
    #########################################################################
    #########################################################################
    # Global variables -
    # Passed back and forth between main function and each menu option function

    # Article_List object, which is a list of Article objects
    # Each Article object contains a name, href, date, tickers, and keywords
    master_articles = Article_List()

    # Dictionary
    # Keys are tickers, Values are either article counts, 'user added', 'file loaded'
    master_tickers = {}

    # Pandas dataframe object
    # Contains tickers associated with company names
    master_ticker_reference = pd.read_csv('ticker_reference.csv')

    # Dictionary
    # Keys are tickers, Values are lists of Pandas dataframe objects containing stock data
    master_stock_data = defaultdict(list)

    # Dictionary
    # Keys are tickers, Values are lists of Pandas dataframe objects containing stock data
    master_stock_data_test = defaultdict(list)

    #########################################################################
    #########################################################################
    #########################################################################
    # Master while loop - continues until user chooses to exit
    while continue_code == True:

        ''' Kyle's stuff commented out for now

        app = Flask(__name__)

        @app.route('/', methods=['GET'])
        def test():
            list = [
                {'param': 'foo', 'val': 2},
                {'param': 'bar', 'val': 10}
            ]
            master_tickers_test = {
                'AMD' : 'user added'
            }
            menu_optionsAPI.get_financial_dataAPI(master_tickers_test, master_stock_data_test, 'manual', [], '2016-01-01','2016-05-01')
            menu_optionsAPI.compute_stock_metricsAPI(master_stock_data_test, 'manual', [])
            print master_stock_data_test
            return  jsonify(results=list)

        if __name__ == "__main__":
            app.run()

        Kyle's stuff commented out for now '''

        #########################################################################
        # Printing main program menu and getting user input on option to execute
        use = \
        menu_options.print_main_menu(master_articles, master_tickers, master_stock_data)

        #########################################################################
        # Option [0] Quick run
        if use == 0:
            menu_options.quick_run(master_articles, master_tickers, master_stock_data, master_ticker_reference)

        #########################################################################
        # Option [1] Load articles
        elif use == 1:
            menu_options.load_articles(master_articles, master_tickers, 'manual', [])

        #########################################################################
        # Option [2] Determine most frequent tickers in loaded articles
        elif use == 2:
            menu_options.determine_top_tickers(master_articles, master_tickers, 'manual', [])

        #########################################################################
        # Option [3] Load tickers from file
        elif use == 3:
            menu_options.load_tickers(master_tickers, 'manual', [])

        #########################################################################
        # Option [4] Create new ticker list file
        elif use == 4:
            menu_options.create_ticker_file(master_tickers, 'manual', [])

        #########################################################################
        # Option [5] View ticker list (and associated articles)
        elif use == 5:
            menu_options.view_ticker_list(master_articles, master_tickers)

        #########################################################################
        # Option [6] Manually edit ticker list
        elif use == 6:
            menu_options.edit_ticker_list(master_tickers, 'manual', [])

        #########################################################################
        # Option [7] Get market data for ticker(s)
        elif use == 7:
            menu_options.get_financial_data(master_tickers, master_stock_data, master_ticker_reference, 'manual', [])

        #########################################################################
        # Option [8] Analyze market data
        elif use == 8:
            menu_options.compute_stock_metrics(master_stock_data, master_ticker_reference, 'manual', [])

        #########################################################################
        # Option [9] Exit program
        elif use == 9:
            menu_options.exit_program()
            continue_code = False

        #########################################################################
        # Error catching
        else:
            print "\nInvalid selection. Please try again."

        ''' Kyle's stuff commented out for now

        f.write('\n----------------------------\n----------------------------\n\n')
        f.write('Kyle Tests\n')
        print master_articles.to_JSON()
        f.write(master_articles.to_JSON())

        # Kyle's html printing
        doc = dominate.document(title='Articles')
        with doc:
            with div():
                ul(li(a(article.name, href=article.href), __pretty=False) for article in master_articles.articles)
        print doc
        with open('articles.html', 'w') as f:
            f.write(doc.render())

        Kyle's stuff commented out for now '''

    # End master while loop
    #########################################################################
    #########################################################################
    #########################################################################
