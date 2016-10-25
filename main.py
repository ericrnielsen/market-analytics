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
import load_articles
from StockInfo import StockInfo

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

    # Variables for the program's overall status
    master_articles = Article_List()
    master_articles_description = ''
    master_tickers = []
    master_stock_data = []

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
        #########################################################################
        # Print main menu information

        # Main menu banner
        print '\n************************************************************'
        print '**********************    MAIN MENU    *********************'
        print '************************************************************'

        # Program status information
        # Articles loaded for analysis
        if len(master_articles) > 0:
            articles_loaded = 'Articles loaded? Yes\n{0}'.format(master_articles_description)
        else:
            articles_loaded = 'Articles loaded? No'

        # Ticker list created
        if len(master_tickers) > 0:
            tickers_identified = 'Ticker list determined? Yes\n'
            tickers_identified += 'Tickers: {0}'.format(', '.join([item[0] for item in master_tickers]))
        else:
            tickers_identified = 'Ticker list determined? No'

        # Stock info obtained (and ready for analysis)
        if len(master_stock_data) > 0:
            info_obtained = 'Market data ready for analysis? Yes\n'
            info_obtained += 'Data available for: {0}\n'.format(', '.join([item.ticker for item in master_stock_data]))
        else:
            info_obtained = 'Market data ready for analysis? No\n'

        # Print status
        print '\nSTATUS'
        print articles_loaded
        print tickers_identified
        print info_obtained

        # Ask user what they want to do with the code
        prompt = '\nWHAT DO YOU WANT TO DO?\n' + \
        '[1] Load articles\n' + \
        '[2] Determine most frequent tickers in loaded articles\n' + \
        '[3] View ticker list (and associated articles)\n' + \
        '[4] Manually edit ticker list\n' + \
        '[5] Get market data for ticker(s)\n' + \
        '[6] Analyze market data\n' + \
        '[7] Exit program\n\n' + \
        'Enter number: '
        use = int(float(raw_input(prompt)))

        #########################################################################
        #########################################################################
        # If user wants to load articles
        if use == 1:
            # Print intro text
            print '\n------------------------------------------------------------'
            print 'Begin [1] Load articles'
            print '------------------------------------------------------------'

            # Ask user if they want to search site(s) live or load articles from previous run
            prompt = '\nHow do you want to load articles?\n[1] Search site(s) live\n' + \
            '[2] Load from previous run\n\nEnter number: '
            choice = int(float(raw_input(prompt)))

            # Make sure user doesn't try to select load from previous run if there are
            # no previous runs available
            if choice == 2 and len(glob2.glob('previous-runs/*.txt')) == 0:
                print '\nNo previous runs available to load from. You will need to search site(s) live.'
                choice = 1

            # If user wants to (or needs to) search live
            if choice == 1:
                master_articles, master_articles_description = load_articles.load_live()

            # Else if user wants to load articles from previous run
            else:
                master_articles, master_articles_description = load_articles.load_previous_run()

            # Need to clear out non-user added top tickers
            master_tickers = [item for item in master_tickers if (item[1] == 'user added')]

            # Print exit text
            print '\n------------------------------------------------------------'
            print 'End [1] Load articles'
            print '------------------------------------------------------------'

        # End use instance of retrieving articles
        #########################################################################
        #########################################################################

        #########################################################################
        #########################################################################
        # If user wants to determine most frequent tickers from loaded articles
        elif use == 2:
            # Print intro text
            print '\n------------------------------------------------------------'
            print 'Begin [2] Determine most frequent tickers in loaded articles'
            print '------------------------------------------------------------'

            # Error check for case that no articles have been loaded
            if len(master_articles) == 0:
                print '\nNo articles loaded. Please load articles and try again.'

            # Else display top ticker information
            else:

                # Ask how many tickers the user would like to know about
                prompt = '\nHow many top tickers would you like to know about? '
                num_top_tickers = int(float(raw_input(prompt)))

                # Get user specified number of most frequent tickers
                top_tickers = master_articles.return_top(num_top_tickers)

                # Need to clear out non-user added top tickers
                master_tickers = [item for item in master_tickers if (item[1] == 'user added')]

                # Add tickers to master ticker list
                top_tickers.reverse()
                for item in top_tickers:
                    if item[0] not in [x[0] for x in master_tickers]:
                        master_tickers.insert(0,item)

            # Print exit text
            print '\n------------------------------------------------------------'
            print 'End [2] Determine most frequent tickers in loaded articles'
            print '------------------------------------------------------------'

        # End use instance user determining most frequent tickers
        #########################################################################
        #########################################################################

        #########################################################################
        #########################################################################
        # If user wants to view ticker list (and associated articles)
        elif use == 3:
            # Print intro text
            print '\n------------------------------------------------------------'
            print 'Begin [3] View ticker list (and associated articles)'
            print '------------------------------------------------------------'

            # Error check for case that no articles have been loaded
            if len(master_tickers) == 0:
                print '\nTicker list is empty.'

            # Else display top ticker information
            else:

                # Display current ticker list and associated article counts
                print '\nCurrent ticker list:'
                n = 1
                for item in master_tickers:
                    print '[{0}] {1:<6} {2}'.format(n, item[0], item[1])
                    n += 1

                # Ask if user would like to see articles associated with tickers
                prompt = '\nDo you want to see the articles associated with each ticker? (Y or N) '
                choice = raw_input(prompt)
                if choice == 'Y' or choice == 'Yes':
                    n = 0
                    for item in master_tickers:
                        n += 1
                        # Print extra new line at beginning of list
                        #if n == 1:
                        #    print ''
                        # For tickers that were added due to article frequency
                        if item[1] != 'user added':
                            print '-----------------------------------------'
                            print '[{0}]/[{1}] All {2} articles for {3}'.format(n, len(master_tickers), item[1], item[0])
                            print '-----------------------------------------'
                            print master_articles.all_for_ticker(item[0])
                        else:
                            print '-----------------------------------------'
                            print '[{0}]/[{1}] {2} was {3}. No articles to display.'.format(n, len(master_tickers), item[0], item[1])
                            print '-----------------------------------------\n'

            # Print exit text
            print '\n------------------------------------------------------------'
            print 'End [3] View ticker list (and associated articles)'
            print '------------------------------------------------------------'

        # End use instance user seeing ticker list and associated articles
        #########################################################################
        #########################################################################

        #########################################################################
        #########################################################################
        # If user wants to edit ticker list
        elif use == 4:
            # Print intro text
            print '\n------------------------------------------------------------'
            print 'Begin [4] Manually edit ticker list'
            print '------------------------------------------------------------'

            # Allow user to edit list as much as they want
            done_editing = False
            while done_editing == False:

                # Display current ticker list and associated article counts
                print '\nCurrent ticker list:'
                n = 1
                for item in master_tickers:
                    print '[{0}] {1}:\t{2}'.format(n, item[0], item[1]).expandtabs(6)
                    n += 1

                # Ask user how they want to edit the list
                prompt = '\nHow do you want to edit the list? (Add or Delete) '
                choice = raw_input(prompt)

                # If user wants to delete
                if choice == 'Delete':
                    prompt = '\nWhat number item do you want to delete? '
                    to_delete = int(float(raw_input(prompt)))
                    if to_delete <= len(master_tickers):
                        master_tickers.pop(to_delete-1)
                    else:
                        print '\nInvalid selection.'

                # If user wants to add
                elif choice == 'Add':
                    prompt = '\nWhat ticker do you want to add? '
                    to_add = raw_input(prompt)
                    master_tickers.append([to_add, 'user added'])

                # Error checking
                else:
                    print '\nInvalid selection.'

                # Ask if the user has any more edits to make
                prompt = '\nDo you want to make any more edits? (Y or N) '
                choice = raw_input(prompt)
                if choice == 'N' or choice == 'No':
                    done_editing = True

            # Print exit text
            print '\n------------------------------------------------------------'
            print 'End [4] Manually edit ticker list'
            print '------------------------------------------------------------'

        # End use instance of user editing ticker list
        #########################################################################
        #########################################################################

        #########################################################################
        #########################################################################
        # If user wants to get market data for ticker(s)
        elif use == 5:
            # Print intro text
            print '\n------------------------------------------------------------'
            print 'Begin [5] Get market data for ticker(s)'
            print '------------------------------------------------------------'

            # Ask user what ticker(s) they want to get info for
            prompt = '\nWhat do you want to do?\n[1] Use all tickers in current ticker list\n' + \
            '[2] Manually enter a single ticker to use\n\nEnter number: '
            ticker_choice = int(float(raw_input(prompt)))

            # Error check if ticker list is empty
            if ticker_choice == 1 and len(master_tickers) == 0:
                print '\nTicker list is empty. Please add tickers and try again.'

            else:
                # If user wants to manually enter a single ticker to use
                if ticker_choice == 2:
                    prompt = '\nWhat ticker do you want to get data for? '
                    tickers_to_use = [raw_input(prompt)]
                # Else if user wants to use all tickers in current ticker list
                else:
                    tickers_to_use = [item[0] for item in master_tickers]

                # Ask user to specify the start date they would like to use
                prompt = '\nEnter start date you would like to use (YYYY-MM-DD): '
                start_date = raw_input(prompt)
                # Change start_date to correct format
                start_year = int(float(start_date.split('-')[0]))
                start_month = int(float(start_date.split('-')[1]))
                start_day = int(float(start_date.split('-')[2]))
                start = datetime.datetime(start_year, start_month, start_day)
                # Ask user to specify the end date they would like to use
                prompt = '\nEnter end date you would like to use (YYYY-MM-DD): '
                end_date = raw_input(prompt)
                # Change end_date to correct format
                end_year = int(float(end_date.split('-')[0]))
                end_month = int(float(end_date.split('-')[1]))
                end_day = int(float(end_date.split('-')[2]))
                end = datetime.datetime(end_year, end_month, end_day)
                # Add StockInfo objects to master_stock_data list
                for item in tickers_to_use:
                    master_stock_data.append(StockInfo(item, start, end))

            # Print exit text
            print '\n------------------------------------------------------------'
            print 'End [5] Get market data for ticker(s)'
            print '------------------------------------------------------------'

        # End use instance of getting market data for ticker(s)
        #########################################################################
        #########################################################################

        #########################################################################
        #########################################################################
        # If user wants to analyze market data
        elif use == 6:
            # Print intro text
            print '\n------------------------------------------------------------'
            print 'Begin [6] Analyze market data'
            print '------------------------------------------------------------'

            # Error check for case that no data available
            if len(master_stock_data) == 0:
                print '\nNo market data available. Please get data and try again.'

            else:
                # Ask user what data they want to analyze (printing list of available data objects)
                prompt = '\nWhat data do you want to analyze?\n'
                n = 0
                for item in master_stock_data:
                    n += 1
                    prompt += '[{0}] {1:<6} '.format(n, item.ticker)
                    prompt += 'data from {0} to {1}\n'.format(str(item.start_date)[:-9], str(item.end_date)[:-9])
                prompt += '\nEnter number: '
                data_choice = int(float(raw_input(prompt)))
                data_choice -= 1

                # Will eventually start analysis here, for now just print
                print '\nTHIS IS TEMPORARY. WILL EVENTUALLY DO ANALYSIS HERE.'
                print 'Market data for {0}'.format(master_stock_data[data_choice].ticker)
                print master_stock_data[data_choice].data

            # Print exit text
            print '\n------------------------------------------------------------'
            print 'End [6] Analyze market data'
            print '------------------------------------------------------------'

        # End use instance of getting info about a stock
        #########################################################################
        #########################################################################

        #########################################################################
        #########################################################################
        # If user wants to quit
        elif use == 7:
            # Print  text
            print '\n------------------------------------------------------------'
            print 'Adios'
            print '------------------------------------------------------------'

            continue_code = False

        # End use instance of user wanting to quit
        #########################################################################
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
