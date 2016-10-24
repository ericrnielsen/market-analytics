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
import retrieve_articles
import get_ticker_info

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

        # Ask user what they want to do with the code
        prompt = '\nWhat do you want to do?\n' + \
        '[1] Retrieve articles\n[2] Get info for ticker\n\nEnter number: '
        use = int(float(raw_input(prompt)))

        #########################################################################
        #########################################################################
        # If user wants to retrieve articles
        if use == 1:

            # Ask user if they want to search site(s) live or load articles from previous run
            prompt = '\nHow do you want to retrieve articles?\n[1] Search site(s) live\n' + \
            '[2] Load from previous run\n\nEnter number: '
            choice = int(float(raw_input(prompt)))

            # Make sure user doesn't try to select load from previous run if there are
            # no previous runs available
            if choice == 2 and len(glob2.glob('previous-runs/all-articles/*.txt')) == 0:
                print '\nNo previous runs available to load from. You will need to search site(s) live.'
                choice = 1

            # If user wants to (or needs to) search live
            if choice == 1:
                master_articles, num_top_tickers = retrieve_articles.load_live()

            # Else if user wants to load articles from previous run
            else:
                master_articles, num_top_tickers = retrieve_articles.load_previous_run()

            # If wanted, print stock stats and article details for specified number of top tickers
            prompt = '\nDo you want to see information about the top tickers? (Y/N) '
            answer = raw_input(prompt)
            if answer == 'Y' or answer == 'Yes':
                retrieve_articles.display_top_tickers(master_articles, num_top_tickers)

            #########################################################################
            # This is where I need to add the link to the stock info!


            #########################################################################

        # End use instance of retrieving articles
        #########################################################################
        #########################################################################


        #########################################################################
        #########################################################################
        # If user wants to get info about a stock
        else:
            # Ask user what ticker they want to get info for
            prompt = '\nEnter the ticker you want to get info for: '
            ticker_choice = raw_input(prompt)

            # Ask user if they want current info or historical info
            prompt = '\nWhat info do you want?\n[1] Current info\n[2] Historical info\n\nEnter number: '
            info_choice = int(float(raw_input(prompt)))

            # If the user selects current info
            if info_choice == 1:
                # Get info
                stock_info = get_ticker_info.get_current(ticker_choice)
                # Print info
                get_ticker_info.print_info(ticker_choice, stock_info)

            # Else if the user selects historical info
            else:
                # Ask user to specify the date range they want to use
                prompt = '\nEnter start date you would like to use (YYYY-MM-DD): '
                start_date = raw_input(prompt)
                prompt = '\nEnter end date you would like to use (YYYY-MM-DD): '
                end_date = raw_input(prompt)
                # Get info
                stock_info = get_ticker_info.get_historical(ticker_choice, start_date, end_date)
                # Print info
                get_ticker_info.print_info(ticker_choice, stock_info)

        # End use instance of getting info about a stock
        #########################################################################
        #########################################################################

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

        #########################################################################
        #########################################################################
        # Ask user if they want to continue using the code of if they want to exit
        prompt = '\n-----------------------------------------------------------\n' + \
        '-----------------------------------------------------------\n\n' + \
        'Do you want to continue with additional actions? (Y/N) '
        answer = raw_input(prompt)
        if answer == 'N' or answer == 'No':
            continue_code = False
            print '\nAdios.\n'

        # End ask if user wants to continue
        #########################################################################
        #########################################################################

    # End master while loop
    #########################################################################
    #########################################################################
    #########################################################################
