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
from load_support import load_live
from load_support import load_previous_run
from StockInfo import StockInfo
import pandas as pd
import openpyxl
from calculation_support import calc_gain
from calculation_support import calc_loss
from calculation_support import calc_spread
from calculation_support import calc_mean
from calculation_support import calc_mov_avg
from calculation_support import calc_high
from calculation_support import calc_low
from calculation_support import calc_per_gain
from calculation_support import calc_rsi_s
from calculation_support import calc_rsi_e
from calculation_support import calc_avg_gain_s
from calculation_support import calc_avg_loss_s
from calculation_support import calc_avg_gain_e
from calculation_support import calc_avg_loss_e
from calculation_support import calc_ema

#########################################################################
#########################################################################
# Start printing main program menu
def print_main_menu(master_articles, master_articles_description, master_tickers, master_stock_data):

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

    # Return items to main function
    return use

# End printing main program menu
#########################################################################
#########################################################################

#########################################################################
#########################################################################
# Start Option [1] Load articles
def load_articles(master_tickers):

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
        master_articles, master_articles_description = load_live()

    # Else if user wants to load articles from previous run
    else:
        master_articles, master_articles_description = load_previous_run()

    # Need to clear out non-user added top tickers
    master_tickers_new = [item for item in master_tickers if (item[1] == 'user added')]

    # Print exit text
    print '\n------------------------------------------------------------'
    print 'End [1] Load articles'
    print '------------------------------------------------------------'

    # Return items to main function
    return master_articles, master_articles_description, master_tickers_new

# End Option [1] Load articles
#########################################################################
#########################################################################

#########################################################################
#########################################################################
# Start Option [2] Determine most frequent tickers in loaded articles
def determine_top_tickers(master_articles, master_tickers):

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
        master_tickers_new = [item for item in master_tickers if (item[1] == 'user added')]

        # Add tickers to master ticker list
        top_tickers.reverse()
        for item in top_tickers:
            if item[0] not in [x[0] for x in master_tickers_new]:
                master_tickers_new.insert(0,item)

    # Print exit text
    print '\n------------------------------------------------------------'
    print 'End [2] Determine most frequent tickers in loaded articles'
    print '------------------------------------------------------------'

    # Return item to main function
    return master_tickers_new

# End Option [2] Determine most frequent tickers in loaded articles
#########################################################################
#########################################################################

#########################################################################
#########################################################################
# Start Option [3] View ticker list (and associated articles)
def view_ticker_list(master_articles, master_tickers):

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

# End Option [3] View ticker list (and associated articles)
#########################################################################
#########################################################################

#########################################################################
#########################################################################
# Start Option [4] Manually edit ticker list
def edit_ticker_list(master_tickers):

    # Print intro text
    print '\n------------------------------------------------------------'
    print 'Begin [4] Manually edit ticker list'
    print '------------------------------------------------------------'

    # Make new master_tickers list that will eventually be returned
    master_tickers_new = master_tickers

    # Allow user to edit list as much as they want
    done_editing = False
    while done_editing == False:

        # Display current ticker list and associated article counts
        print '\nCurrent ticker list:'
        n = 1
        for item in master_tickers_new:
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
                master_tickers_new.pop(to_delete-1)
            else:
                print '\nInvalid selection.'

        # If user wants to add
        elif choice == 'Add':
            prompt = '\nWhat ticker do you want to add? '
            to_add = raw_input(prompt)
            master_tickers_new.append([to_add, 'user added'])

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

    # Return item to main function
    return master_tickers_new

# End Option [4] Manually edit ticker list
#########################################################################
#########################################################################

#########################################################################
#########################################################################
# Start Option [5] Get market data for ticker(s)
def get_market_data(master_tickers, master_stock_data):

    # Print intro text
    print '\n------------------------------------------------------------'
    print 'Begin [5] Get market data for ticker(s)'
    print '------------------------------------------------------------'

    # Make new master_stock_data list that will eventually be returned
    master_stock_data_new = master_stock_data

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
            master_stock_data_new.append(StockInfo(item, start, end))

    # Print exit text
    print '\n------------------------------------------------------------'
    print 'End [5] Get market data for ticker(s)'
    print '------------------------------------------------------------'

    # Return item to main function
    return master_stock_data_new

# End Option [5] Get market data for ticker(s)
#########################################################################
#########################################################################

#########################################################################
#########################################################################
# Start Option [6] Analyze market data
# THIS STILL NEEDS TO BE FULLY IMPLEMENTED
def analyze_market_data(master_stock_data):

    # Tells pandas not to limit # columns in printing
    pd.set_option('expand_frame_repr', False)
    pd.set_option('display.max_rows', 50)
    pd.set_option('display.max_columns', 50)

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

        # df_ticker = ticker for the current object, df_data = all the actual data
        df_ticker = master_stock_data[data_choice].ticker
        df_data = master_stock_data[data_choice].data

        # Reverse the data so it's in decending order
        df_data = df_data.sort_index(axis=0 ,ascending=False)

        # Make new column containing dates (currently in index)
        df_data['Date'] = df_data.index
        cols = df_data.columns.tolist()
        cols.insert(0, cols.pop(cols.index('Date')))
        df_data = df_data.reindex(columns= cols)

        # Make index be a count up from 0
        indices = range(0, len(df_data.index))
        df_data.index = indices

        # Create list with names of additional columns to be added to the table
        columns_to_add = ['Spread', 'Gain', 'Loss', \
        '10 MA', '10 MA %', '15 MA', '15 MA %', '20 MA', '20 MA %', \
        '50 MA', '50 MA %', '100 MA', '100 MA %', '200 MA', '200 MA %', \
        '10 EMA', '20 EMA', '50 EMA', \
        '52 Wk. High', '52 Wk. Low', \
        '14 Sim. Avg. Gain', '14 Exp. Avg. Gain', '14 Sim. Avg. Loss', '14 Exp. Avg. Loss', \
        '28 Sim. Avg. Gain', '28 Exp. Avg. Gain', '28 Sim. Avg. Loss', '28 Exp. Avg. Loss', \
        '42 Sim. Avg. Gain', '42 Exp. Avg. Gain', '42 Sim. Avg. Loss', '42 Exp. Avg. Loss', \
        '56 Sim. Avg. Gain', '56 Exp. Avg. Gain', '56 Sim. Avg. Loss', '56 Exp. Avg. Loss', \
        '14 Sim. RSI', '14 Exp. RSI', '28 Sim. RSI', '28 Exp. RSI',
        '42 Sim. RSI', '42 Exp. RSI', '56 Sim. RSI', '56 Exp. RSI']

        # Initialize additional column values to be 0.0
        for label in columns_to_add:
             df_data[label] = 0.0

        # Add values to spread column
        df_data ['Spread'] = calc_spread(df_data)

        # Add values to gain and loss columns
        df_data['Gain'] = calc_gain(df_data)
        df_data['Loss'] = calc_loss(df_data)

        # Create lists with days to be used for the various calculations
        MA_days = [10, 15, 20, 50, 100, 200]
        EMA_days = [10, 20, 50]
        RSI_days = [14, 28, 42, 56]

        ##############################################################
        ##############################################################
        # Start loop 1 to fill columns
        for index, row in df_data.iterrows():

            # Getting 52 week high
            df_data.set_value(index, '52 Wk. High', calc_high(df_data, index, 52*5))

            # Getting 52 week low
            df_data.set_value(index, '52 Wk. Low', calc_low(df_data, index, 52*5))

            # Getting 10, 15, 50, 100, 200 day moving average
            for days in MA_days:
                column = str(days) + ' MA'
                df_data.set_value(index, column, calc_mov_avg(df_data, index, days))

            # Geting simple average gains and losses to be used later for RSI calcs
            for days in RSI_days:
                column_gain = str(days) + ' Sim. Avg. Gain'
                column_loss = str(days) + ' Sim. Avg. Loss'
                df_data.set_value(index, column_gain, calc_avg_gain_s(df_data, index, days))
                df_data.set_value(index, column_loss, calc_avg_loss_s(df_data, index, days))

        # End loop 1 to fill columns
        ##############################################################
        ##############################################################

        ##############################################################
        ##############################################################
        # Start loop 2 to fill columns
        for index in df_data.index:

            # Getting 10, 15, 50, 100, 200 day percent gains
            for days in MA_days:
                column = str(days) + ' MA %'
                df_data.set_value(index, column, calc_per_gain(df_data, index, days))

        # End loop 2 to fill columns
        ##############################################################
        ##############################################################

        # Flip table prior to calculating EMAs and exponential avg. gains and losses
        df_data = df_data.sort_index(axis=0 ,ascending=False)

        ##############################################################
        ##############################################################
        # Start loop 3 to fill columns
        for index in df_data.index:

            # Getting 10, 20, and 50 day EMA values
            for days in EMA_days:
                column = str(days) + ' EMA'
                df_data.set_value(index, column, calc_ema(df_data, index, days))

            # Geting exponential average gains and losses to be used later for RSI calcs
            for days in RSI_days:
                column_gain = str(days) + ' Exp. Avg. Gain'
                column_loss = str(days) + ' Exp. Avg. Loss'
                df_data.set_value(index, column_gain, calc_avg_gain_e(df_data, index, days))
                df_data.set_value(index, column_loss, calc_avg_loss_e(df_data, index, days))

        # End loop 3 to fill columns
        ##############################################################
        ##############################################################

        # Flip table back to be ordered newest date to oldest date
        df_data = df_data.sort_index(axis=0 ,ascending=True)

        ##############################################################
        ##############################################################
        # Start loop 4 to fill columns
        for index, row in df_data.iterrows():

            # Getting 14, 28, 42, 56 day simple and exponential RSIs
            for days in RSI_days:
                column_s = str(days) + ' Sim. RSI'
                column_e = str(days) + ' Exp. RSI'
                df_data.set_value(index, column_s, calc_rsi_s(df_data, index, days))
                df_data.set_value(index, column_e, calc_rsi_e(df_data, index, days))

        # End loop 4 to fill columns
        ##############################################################
        ##############################################################

        # EMA
        # Start at bottom
        # Use the normal MA as the first value
        # To avoid recurssion
        # Then work backward using formula
        # Make a 20 day moving average to work with the 20 day EMA

        # Add 52 week range
        # Add average volume

        # Send output of the calculations to Excel
        excel_output = df_ticker + ' data.xlsx'
        writer = pd.ExcelWriter(excel_output)
        df_data.to_excel(writer,'Sheet1')
        writer.save()

        # Will eventually start analysis here, for now just print
        print '\nData saved to {0}'.format(excel_output)
        #print 'Market data for {0}'.format(df_ticker)
        #print df_data

        # Return item to main function
        return df_data

    # Print exit text
    print '\n------------------------------------------------------------'
    print 'End [6] Analyze market data'
    print '------------------------------------------------------------'

# End Option [6] Analyze market data
#########################################################################
#########################################################################

#########################################################################
#########################################################################
# Start Option [7] Exit program
def exit_program():

    # Print  text
    print '\n------------------------------------------------------------'
    print 'Adios'
    print '------------------------------------------------------------'

# End Option [7] Exit program
#########################################################################
#########################################################################
