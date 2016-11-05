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
from collections import defaultdict
import pandas as pd
import ticker_reference

# Kyle's stuff commented out for now
'''
class form:
    form = web.form.Form(
        web.form.Checkbox('zergwatch', value=True),
        web.form.Checkbox('streetupdates', value=True),
        web.form.Checkbox('newsoracle', value=True),
        web.form.Checkbox('smarteranalyst', value=True),
        web.form.Checkbox('streetinsider', value=True),
        web.form.Dropdown('days', args=['1', '2', '3', '4', '5']),
        web.form.Button('Post entry')
    )

    # GET method is used when there is no form data sent to the server
    def GET(self):
        form = self.form()
        return render.form(form)

    def POST(self):
        form = self.form()
        if not form.validates():
            print 'uh oh'
        raise web.seeother('/success')
'''

if __name__ == "__main__":

    # Variable that allows the code to loop until the user chooses to exit
    continue_code = True

    # Overarching variables
    # (passed back and forth between main function and each menu option function)
    master_articles = Article_List()
    #master_tickers = defaultdict(list)
    master_tickers = {}
    master_ticker_reference = pd.read_csv('ticker_reference.csv')
    master_stock_data = defaultdict(list)

    #########################################################################
    #########################################################################
    #########################################################################
    # Master while loop - continues until user chooses to exit
    while continue_code == True:

        # Kyle's stuff commented out for now
        # Eric, change this if you dont want to use the server for inputs
        '''
        server = False

        urls = (
            '/articles', 'form'
        )
        render = web.template.render('templates/')
        app = web.application(urls, globals())
        if server:
            app.run()
        '''

        #########################################################################
        # Printing main program menu and getting user input on option to execute
        use = \
        menu_options.print_main_menu(master_articles, master_tickers, master_stock_data)

        #########################################################################
        # Option [0] Quick run
        if use == 0:
            menu_options.quick_run(master_articles, master_tickers, master_stock_data)

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
            menu_options.get_financial_data(master_tickers, master_stock_data, 'manual', [])

        #########################################################################
        # Option [8] Analyze market data
        elif use == 8:
            menu_options.compute_stock_metrics(master_stock_data, 'manual', [])

        #########################################################################
        # Option [9] Load stock metrics from Excel file
        elif use == 9:
            menu_options.load_stock_metrics(master_stock_data, 'manual', [])

        #########################################################################
        # Option [10] Exit program
        elif use == 10:
            menu_options.exit_program()
            continue_code = False

        #########################################################################
        # Error catching
        else:
            print "\nInvalid selection. Please try again."

        # Kyle's stuff commented out for now
        '''
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
        '''

    # End master while loop
    #########################################################################
    #########################################################################
    #########################################################################
