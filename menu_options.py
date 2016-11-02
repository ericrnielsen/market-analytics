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
def print_main_menu(master_articles, master_tickers, master_stock_data):

    # Main menu banner
    print '\n************************************************************'
    print '**********************    MAIN MENU    *********************'
    print '************************************************************'

    # Program status information
    # Articles loaded for analysis
    if len(master_articles) > 0:
        articles_loaded = 'Articles loaded? Yes\n{0}'.format(master_articles.description)
    else:
        articles_loaded = 'Articles loaded? No'

    # Ticker list created
    if len(master_tickers) > 0:
        sorted_tickers = sorted(master_tickers.items(), key=operator.itemgetter(1))
        sorted_tickers.reverse()
        tickers_identified = 'Ticker list determined? Yes\n'
        tickers_identified += 'Tickers: {0}'.format(', '.join(['{0} ({1})'.format(item[0], item[1]) for item in sorted_tickers]))
    else:
        tickers_identified = 'Ticker list determined? No'

    # Stock info obtained (and ready for computation)
    ready_tickers = []
    for ticker in master_stock_data:
        for data_set in master_stock_data[ticker]:
            if data_set.data_type == 'base' and data_set.ticker not in ready_tickers:
                ready_tickers.append(data_set.ticker)
    if len(ready_tickers) > 0:
        info_obtained = 'Market data ready for computation? Yes\n'
        info_obtained += 'Data available for: {0}'.format(', '.join(ready_tickers))
    else:
        info_obtained = 'Market data ready for computation? No'

    # Stock info computed (additional columns added to tableframe)
    computed_tickers = []
    for ticker in master_stock_data:
        for data_set in master_stock_data[ticker]:
            if data_set.data_type == 'computed' and data_set.ticker not in computed_tickers:
                computed_tickers.append(data_set.ticker)
    if len(computed_tickers) > 0:
        info_computed = 'Stock metrics computed? Yes\n'
        info_computed += 'Data computed for: {0}\n'.format(', '.join(computed_tickers))
    else:
        info_computed = 'Stock metrics computed? No\n'

    # Print status
    print '\nSTATUS'
    print articles_loaded
    print tickers_identified
    print info_obtained
    print info_computed

    # Ask user what they want to do with the code
    prompt = '\nWHAT DO YOU WANT TO DO?\n' + \
    '[0] Quick run\n' + \
    '[1] Load articles\n' + \
    '[2] Determine most frequent tickers in loaded articles\n' + \
    '[3] View ticker list (and associated articles)\n' + \
    '[4] Manually edit ticker list\n' + \
    '[5] Get financial data for ticker(s)\n' + \
    '[6] Compute stock metrics\n' + \
    '[7] Exit program\n\n' + \
    'Enter number: '
    try:
        use = int(float(raw_input(prompt)))
    except:
        use = -1

    # Return items to main function
    return use

# End printing main program menu
#########################################################################
#########################################################################

#########################################################################
#########################################################################
# Start Option [0] Quick run
def quick_run(master_articles, master_tickers, master_stock_data):

    # Print intro text
    print '\n------------------------------------------------------------'
    print 'Begin [0] Quick run'
    print '------------------------------------------------------------'

    # Ask user what type of quick run they want to do
    prompt = '\nWhich quick run do you want to do?\n' + \
    '[1] Search streetinsider live -> determine top tickers -> get financial data\n' + \
    '[2] Enter ticker(s) -> get financial data\n' + \
    '[3] Current test configuration (TWX from 2015-01-01 to today)\n\n' + \
    'Enter number: '
    choice = int(float(raw_input(prompt)))

    # Create dictionary of automated selections that will be passed to functions
    selections = {}
    selections['Quickrun'] = 0
    selections['Days to Search'] = 0
    selections['Num Top Tickers'] = 0
    selections['Tickers'] = []
    selections['Start'] = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    selections['End'] = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

    # If user selects option 1
    if choice == 1:
        # Need to get all input necessary to make function calls
        prompt1 = raw_input("\nHow many days back do you want to search? ")
        days_to_search = int(float(prompt1))
        prompt2 = '\nHow many top tickers would you like to identify? '
        num_top_tickers = int(float(raw_input(prompt2)))
        prompt3 = '\nHow many years of financial data would you like to get? '
        data_years = int(float(raw_input(prompt3)))

        # Fill selections list to be passed to required functions
        selections['Quickrun'] = 1
        selections['Days to Search'] = days_to_search
        selections['Num Top Tickers'] = num_top_tickers
        selections['Start'] = selections['End'] - datetime.timedelta(days=(365*data_years))

        # Load articles from streetinsider
        load_articles(master_articles, master_tickers, 'quick', selections)

        # Need to clear out non-user added top tickers
        for key, value in master_tickers.items():
            if value != 'user added':
                del master_tickers[key]

        # Determine top tickers
        determine_top_tickers(master_articles, master_tickers, 'quick', selections)
        for key, value in master_tickers.items():
            if value != 'user added':
                selections['Tickers'].append(key)

        # Get market data for identified tickers
        get_financial_data(master_tickers, master_stock_data, 'quick', selections)

        # Analyze market data (do calculations) for identified tickers
        compute_stock_metrics(master_stock_data, 'quick', selections)

    # If user selects option 2
    elif choice == 2:
        # Need to get all input necessary to make function calls
        prompt1 = '\nWhat tickers would you like to get financial data for? '
        desired_tickers = raw_input(prompt1).split(' ')
        prompt2 = '\nHow many years of financial data would you like to get? '
        data_years = int(float(raw_input(prompt2)))

        # Fill selections list to be passed to required functions
        selections['Quickrun'] = 2
        selections['Start'] = selections['End'] - datetime.timedelta(days=(365*data_years))
        for ticker in desired_tickers:
            selections['Tickers'].append(ticker)

        # Add tickers to ticker list
        edit_ticker_list(master_tickers, 'quick', selections)

        # Get market data for identified tickers
        get_financial_data(master_tickers, master_stock_data, 'quick', selections)

        # Analyze market data (do calculations) for identified tickers
        compute_stock_metrics(master_stock_data, 'quick', selections)

    # If user selects option 3
    else:
        # Fill selections list to be passed to required functions
        selections['Quickrun'] = 3
        selections['Start'] = datetime.datetime(2015, 01, 01)
        selections['Tickers'].append('TWX')

        # Add tickers to ticker list
        edit_ticker_list(master_tickers, 'quick', selections)

        # Get market data for identified tickers
        get_financial_data(master_tickers, master_stock_data, 'quick', selections)

        # Analyze market data (do calculations) for identified tickers
        compute_stock_metrics(master_stock_data, 'quick', selections)

    # Print exit text
    print '\n------------------------------------------------------------'
    print 'End [0] Quick run'
    print '------------------------------------------------------------'

# End Option [0] Quick run
#########################################################################
#########################################################################

#########################################################################
#########################################################################
# Start Option [1] Load articles
def load_articles(master_articles, master_tickers, run_type, selections):

    # Print intro text
    print '\n------------------------------------------------------------'
    print 'Begin [1] Load articles (' + run_type + ')'
    print '------------------------------------------------------------'

    # If need to get user input manually (not a quick run)
    if run_type == 'manual':
        # Ask user if they want to search site(s) live or load articles from previous run
        prompt = '\nHow do you want to load articles?\n[1] Search site(s) live\n' + \
        '[2] Load from previous run\n\nEnter number: '
        choice = int(float(raw_input(prompt)))

        # Make sure user doesn't try to select load from previous run if there are
        # no previous runs available
        if choice == 2 and len(glob2.glob('previous-runs/*.txt')) == 0:
            print '\nNo previous runs available to load from. You will need to search site(s) live.'
            choice = 1

    # Else it's a quick run so user inputs already entered
    else:
        choice = 1

    # If user wants to (or needs to) search live
    if choice == 1:
        if run_type == 'manual':
            load_live(master_articles, 'manual', {})
        else:
            load_live(master_articles, 'quick', selections)

    # Else if user wants to load articles from previous run
    else:
        load_previous_run(master_articles)

    # Need to clear out non-user added top tickers
    for key, value in master_tickers.items():
        if value != 'user added':
            del master_tickers[key]

    # Print exit text
    print '\n------------------------------------------------------------'
    print 'End [1] Load articles (' + run_type + ')'
    print '------------------------------------------------------------'

# End Option [1] Load articles
#########################################################################
#########################################################################

#########################################################################
#########################################################################
# Start Option [2] Determine most frequent tickers in loaded articles
def determine_top_tickers(master_articles, master_tickers, run_type, selections):

    # Print intro text
    print '\n------------------------------------------------------------'
    print 'Begin [2] Determine most frequent tickers in loaded articles (' + run_type + ')'
    print '------------------------------------------------------------'

    # Error check for case that no articles have been loaded
    if len(master_articles) == 0:
        print '\nNo articles loaded. Please load articles and try again.'

    # Else determine user specified number of top tickers
    else:

        # If need to get user input manually (not a quick run)
        if run_type == 'manual':
            # Ask how many tickers the user would like to know about
            prompt = '\nHow many top tickers would you like to know about? '
            num_top_tickers = int(float(raw_input(prompt)))

        # Else it's a quick run so user inputs already entered
        else:
            num_top_tickers = selections['Num Top Tickers']

        # Get user specified number of most frequent tickers
        top_tickers = master_articles.return_top(num_top_tickers)

        # Need to clear out non-user added top tickers
        for key, value in master_tickers.items():
            if value != 'user added':
                del master_tickers[key]

        # Add tickers to master ticker list
        for key in top_tickers:
            master_tickers[key] = top_tickers[key]

    # Print exit text
    print '\n------------------------------------------------------------'
    print 'End [2] Determine most frequent tickers in loaded articles (' + run_type + ')'
    print '------------------------------------------------------------'

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

        # Create ordered list of top tickers
        sorted_tickers = sorted(master_tickers.items(), key=operator.itemgetter(1))
        sorted_tickers.reverse()

        # Display current ticker list and associated article counts
        print '\nCurrent ticker list:'
        n = 1
        for item in sorted_tickers:
            print '[{0}] {1:<6} {2}'.format(n, item[0], item[1])
            n += 1

        # Ask if user would like to see articles associated with tickers
        prompt = '\nDo you want to see the articles associated with each ticker? (Y or N) '
        choice = raw_input(prompt)
        if choice == 'Y' or choice == 'Yes':
            n = 0
            for item in sorted_tickers:
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
def edit_ticker_list(master_tickers, run_type, selections):

    # Print intro text
    print '\n------------------------------------------------------------'
    print 'Begin [4] Manually edit ticker list (' + run_type + ')'
    print '------------------------------------------------------------'

    # If need to get user input manually (not a quick run)
    if run_type == 'manual':
        # Allow user to edit list as much as they want
        done_editing = False
        while done_editing == False:

            # Create ordered list of top tickers
            sorted_tickers = sorted(master_tickers.items(), key=operator.itemgetter(1))
            sorted_tickers.reverse()

            # Display current ticker list and associated article counts
            print '\nCurrent ticker list:'
            n = 1
            for item in sorted_tickers:
                print '[{0}] {1:<6} {2}'.format(n, item[0], item[1])
                n += 1

            # Ask user how they want to edit the list
            prompt = '\nHow do you want to edit the list? (Add or Delete) '
            choice = raw_input(prompt)

            # If user wants to delete
            if choice == 'Delete':
                prompt = '\nWhat number item do you want to delete? '
                num_to_delete = int(float(raw_input(prompt)))
                if num_to_delete <= len(sorted_tickers):
                    ticker_to_delete = sorted_tickers[num_to_delete-1][0]
                    del master_tickers[ticker_to_delete]
                else:
                    print '\nInvalid selection.'

            # If user wants to add
            elif choice == 'Add':
                prompt = '\nWhat ticker do you want to add? '
                ticker_to_add = raw_input(prompt)
                master_tickers[ticker_to_add] = 'user added'

            # Error checking
            else:
                print '\nInvalid selection.'

            # Ask if the user has any more edits to make
            prompt = '\nDo you want to make any more edits? (Y or N) '
            choice = raw_input(prompt)
            if choice == 'N' or choice == 'No':
                done_editing = True

    # Else it's a quick run so user inputs already entered
    else:
        for ticker_to_add in selections['Tickers']:
            master_tickers[ticker_to_add] = 'user added'

    # Print exit text
    print '\n------------------------------------------------------------'
    print 'End [4] Manually edit ticker list (' + run_type + ')'
    print '------------------------------------------------------------'

# End Option [4] Manually edit ticker list
#########################################################################
#########################################################################

#########################################################################
#########################################################################
# Start Option [5] Get financial data for ticker(s)
def get_financial_data(master_tickers, master_stock_data, run_type, selections):

    # Print intro text
    print '\n------------------------------------------------------------'
    print 'Begin [5] Get financial data for ticker(s) (' + run_type + ')'
    print '------------------------------------------------------------'

    # If need to get user input manually (not a quick run)
    if run_type == 'manual':
        # Ask user what ticker(s) they want to get info for
        prompt = '\nWhat do you want to do?\n[1] Use all tickers in current ticker list\n' + \
        '[2] Manually enter ticker(s) to use\n\nEnter number: '
        ticker_choice = int(float(raw_input(prompt)))

        # Error check if ticker list is empty
        if ticker_choice == 1 and len(master_tickers) == 0:
            print '\nTicker list is empty. Please add tickers and try again.'

        else:
            # If user wants to manually enter ticker(s) to use
            if ticker_choice == 2:
                prompt = '\nWhat ticker(s) do you want to get data for? '
                tickers_to_use = raw_input(prompt).split(' ')
            # Else if user wants to use all tickers in current ticker list
            else:
                tickers_to_use = [item for item in master_tickers.keys()]

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
            for ticker in tickers_to_use:
                master_stock_data[ticker].append(StockInfo(ticker, start, end))

    # Else it's a quick run so user inputs already entered
    else:
        tickers_to_use = selections['Tickers']
        start = selections['Start']
        end = selections['End']
        for ticker in tickers_to_use:
            master_stock_data[ticker].append(StockInfo(ticker, start, end))

    # Print exit text
    print '\n------------------------------------------------------------'
    print 'End [5] Get financial data for ticker(s) (' + run_type + ')'
    print '------------------------------------------------------------'

# End Option [5] Get financial data for ticker(s)
#########################################################################
#########################################################################

#########################################################################
#########################################################################
# Start Option [6] Compute stock metrics
def compute_stock_metrics(master_stock_data, run_type, selections):

    # Print intro text
    print '\n------------------------------------------------------------'
    print 'Begin [6] Compute stock metrics (' + run_type + ')'
    print '------------------------------------------------------------'

    # Error check for case that no data available
    if len(master_stock_data) == 0:
        print '\nNo market data available. Please get data and try again.'

    else:
        # If need to get user input manually (not a quick run)
        if run_type == 'manual':
            # Ask user what data they want to analyze (printing list of available data objects)
            prompt = '\nWhat data do you want to analyze?\n'
            n = 0
            possible_compute = {}
            for ticker in master_stock_data:
                data_set_index = -1
                for data_set in master_stock_data[ticker]:
                    data_set_index += 1
                    if data_set.data_type == 'base':
                        n += 1
                        prompt += '[{0}] {1:<6} '.format(n, data_set.ticker)
                        prompt += 'data from {0} to {1}\n'.format(str(data_set.start_date)[:-9], str(data_set.end_date)[:-9])
                        possible_compute[n] = [ticker, data_set_index, data_set]
            prompt += '\nEnter number(s): '
            choices = (raw_input(prompt).split(' '))
            chosen_compute = []
            for num in choices:
                chosen_compute.append(possible_compute[int(float(num))])

        # Else it's a quick run so user inputs already entered
        else:
            chosen_compute = []
            for ticker in master_stock_data:
                if ticker in selections['Tickers']:
                    data_set_index = -1
                    for data_set in master_stock_data[ticker]:
                        data_set_index += 1
                        if data_set.data_type == 'base' and data_set.start_date == selections['Start'] and data_set.end_date == selections['End']:
                            chosen_compute.append([ticker, data_set_index, data_set])

        ##############################################################
        ##############################################################
        # Start loop through analysis for all tickers selected
        for chosen in chosen_compute:

            # Easy references for the 3 components of 'chosen'
            current_ticker = chosen[0]
            current_data_set_index = chosen[1]
            current_data_set = chosen [2]

            # df_ticker = ticker for the current object, df_data = all the actual data
            df_ticker = current_data_set.ticker
            df_data = current_data_set.data

            # Reverse the data so it's in decending order
            df_data = df_data.sort_index(axis=0 ,ascending=False)

            # If the dataframe object for the ticker
            if len(df_data.columns.tolist()) == 6:
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

            # Send output of the calculations to Excel
            first = str(df_data['Date'][0])[:-9]
            last = str(df_data['Date'][len(df_data.index) - 1])[:-9]
            excel_output = 'stock-data/' + df_ticker + '_' + last + '_to_' + first + '.xlsx'
            writer = pd.ExcelWriter(excel_output)
            df_data.to_excel(writer,'Sheet1')
            writer.save()
            print '\nData saved to {0}'.format(excel_output)

            # Re-assign data in StockInfo object as updated dataframe table
            master_stock_data[current_ticker][current_data_set_index].add_metrics(df_data)

        # End loop through analysis for all tickers selected
        ##############################################################
        ##############################################################

    # Print exit text
    print '\n------------------------------------------------------------'
    print 'End [6] Compute stock metrics (' + run_type + ')'
    print '------------------------------------------------------------'

# End Option [6] Compute stock metrics
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
