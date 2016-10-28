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
import load_support
from StockInfo import StockInfo
import pandas as pd
from calculation_support import calc_gain
from calculation_support import calc_loss
from calculation_support import calc_mean


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
        master_articles, master_articles_description = load_support.load_live()

    # Else if user wants to load articles from previous run
    else:
        master_articles, master_articles_description = load_support.load_previous_run()

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

        # Add spread column
        df_data['Spread'] = df_data['High'] - df_data['Low']

        # Add gain and loss columns
        df_data['Gain'] = df_data.apply(lambda row: calc_gain(row['Open'], row['Close']), axis=1)
        df_data['Loss'] = df_data.apply(lambda row: calc_loss(row['Open'], row['Close']), axis=1)

        # Initializing additional columns
        df_data['10Avg'] = 0.0
        df_data['10Per'] = 0.0
        df_data['15Avg'] = 0.0
        df_data['15Per'] = 0.0
        df_data['50Avg'] = 0.0
        df_data['50Per'] = 0.0
        df_data['100Avg'] = 0.0
        df_data['100Per'] = 0.0
        df_data['200Avg'] = 0.0
        df_data['200Per'] = 0.0
        df_data['52DHigh'] = 0.0
        df_data['52DLow'] = 0.0
        df_data['14RSI'] = 0.0
        df_data['28RSI'] = 0.0
        df_data['42RSI'] = 0.0
        df_data['56RSI'] = 0.0

        ##############################################################
        ##############################################################
        # Start loop 1 to fill columns
        for index, row in df_data.iterrows():
            # Getting 10, 15, 50, 100, 200 day moving average
            current_slice_10 = df_data[index:index+10]
            current_slice_15 = df_data[index:index+15]
            current_slice_50 = df_data[index:index+50]
            current_slice_100 = df_data[index:index+100]
            current_slice_200 = df_data[index:index+200]

            mean_10 = current_slice_10['Adj Close'].mean()
            mean_15 = current_slice_15['Adj Close'].mean()
            mean_50 = current_slice_50['Adj Close'].mean()
            mean_100 = current_slice_100['Adj Close'].mean()
            mean_200 = current_slice_200['Adj Close'].mean()

            df_data.set_value(index, '10Avg', mean_10)
            df_data.set_value(index, '15Avg', mean_15)
            df_data.set_value(index, '50Avg', mean_50)
            df_data.set_value(index, '100Avg', mean_100)
            df_data.set_value(index, '200Avg', mean_200)

            # Getting 52 week high
            current_slice_52 = df_data[index:index+52]
            high_52 = current_slice_52['Adj Close'].max()
            df_data.set_value(index, '52DHigh', high_52)

            # Getting 52 week low
            low_52 = current_slice_52['Adj Close'].min()
            df_data.set_value(index, '52DLow', low_52)

        # End loop 1 to fill columns
        ##############################################################
        ##############################################################

        ##############################################################
        ##############################################################
        # Start loop 2 to fill columns
        for index in df_data.index:
            # Getting 10, 15, 50, 100, 200 day percent gains
            try:
                # 10, 15, 50, 100, and 200 day moving averages percent gains
                today_10 = df_data.get_value(index, '10Avg')
                today_15 = df_data.get_value(index, '15Avg')
                today_50 = df_data.get_value(index, '50Avg')
                today_100 = df_data.get_value(index, '100Avg')
                today_200 = df_data.get_value(index, '200Avg')

                yesterday_10 = df_data.get_value(index+1, '10Avg')
                yesterday_15 = df_data.get_value(index+1, '15Avg')
                yesterday_50 = df_data.get_value(index+1, '50Avg')
                yesterday_100 = df_data.get_value(index+1, '100Avg')
                yesterday_200 = df_data.get_value(index+1, '200Avg')

                gain_10 = ((today_10 / yesterday_10) - 1) * 100
                gain_15 = ((today_15 / yesterday_15) - 1) * 100
                gain_50 = ((today_50 / yesterday_50) - 1) * 100
                gain_100 = ((today_100 / yesterday_100) - 1) * 100
                gain_200 = ((today_200 / yesterday_200) - 1) * 100

            except:
                gain_10 = None
                gain_15 = None
                gain_50 = None
                gain_100 = None
                gain_200 = None

            df_data.set_value(index, '10Per', gain_10)
            df_data.set_value(index, '15Per', gain_15)
            df_data.set_value(index, '50Per', gain_50)
            df_data.set_value(index, '100Per', gain_100)
            df_data.set_value(index, '200Per', gain_200)
        # End loop 2 to fill columns
        ##############################################################
        ##############################################################

        ##############################################################
        ##############################################################
        # Start loop 3 to fill columns
        for index, row in df_data.iterrows():
            # Getting 14, 28, 42, 56 day RPIs
            current_slice_14 = df_data[index:index+14]
            current_slice_28 = df_data[index:index+28]
            current_slice_42 = df_data[index:index+42]
            current_slice_56 = df_data[index:index+56]

            gain_values_14 = []
            loss_values_14 = []
            gain_values_28 = []
            loss_values_28 = []
            gain_values_42 = []
            loss_values_42 = []
            gain_values_56 = []
            loss_values_56 = []

            for index_14 in current_slice_14.index:
                current_gain = df_data.get_value(index_14, 'Gain')
                current_loss = df_data.get_value(index_14, 'Loss')
                if current_gain != 0:
                    gain_values_14.append(current_gain)
                if current_loss != 0:
                    loss_values_14.append(current_loss)

            for index_28 in current_slice_28.index:
                current_gain = df_data.get_value(index_28, 'Gain')
                current_loss = df_data.get_value(index_28, 'Loss')
                if current_gain != 0:
                    gain_values_28.append(current_gain)
                if current_loss != 0:
                    loss_values_28.append(current_loss)

            for index_42 in current_slice_42.index:
                current_gain = df_data.get_value(index_42, 'Gain')
                current_loss = df_data.get_value(index_42, 'Loss')
                if current_gain != 0:
                    gain_values_42.append(current_gain)
                if current_loss != 0:
                    loss_values_42.append(current_loss)

            for index_56 in current_slice_56.index:
                current_gain = df_data.get_value(index_56, 'Gain')
                current_loss = df_data.get_value(index_56, 'Loss')
                if current_gain != 0:
                    gain_values_56.append(current_gain)
                if current_loss != 0:
                    loss_values_56.append(current_loss)

            gain_avg_14, loss_avg_14 = calc_mean(gain_values_14), calc_mean(loss_values_14)
            gain_avg_28, loss_avg_28 = calc_mean(gain_values_28), calc_mean(loss_values_28)
            gain_avg_42, loss_avg_42 = calc_mean(gain_values_42), calc_mean(loss_values_42)
            gain_avg_56, loss_avg_56 = calc_mean(gain_values_56), calc_mean(loss_values_56)

            rsi_14 = 100 - (100 / (1 + gain_avg_14/loss_avg_14))
            rsi_28 = 100 - (100 / (1 + gain_avg_28/loss_avg_28))
            rsi_42 = 100 - (100 / (1 + gain_avg_42/loss_avg_42))
            rsi_56 = 100 - (100 / (1 + gain_avg_56/loss_avg_56))

            df_data.set_value(index, '14RSI', rsi_14)
            df_data.set_value(index, '28RSI', rsi_28)
            df_data.set_value(index, '42RSI', rsi_42)
            df_data.set_value(index, '56RSI', rsi_56)

        # End loop 3 to fill columns
        ##############################################################
        ##############################################################

        # EMA
        # Start at bottom
        # Use the normal MA as the first value
        # To avoid recurssion
        # Then work backward using formula
        # Make a 20 day moving average to work with the 20 day EMA

        # RSI
        # When it approaches 70, you know the stock is going to tank
        # Then it will drop a lot, but you still have a little time before the price goes down

        # Add 52 week range
        # Add average volume

        # Will eventually start analysis here, for now just print
        print '\nTHIS IS TEMPORARY. WILL EVENTUALLY DO ANALYSIS HERE.'
        print 'Market data for {0}'.format(df_ticker)
        print df_data

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
