#!/usr/bin/python

import sys
import datetime
import dominate
from dominate.tags import *
import xlrd
import os
import glob2
import pandas as pd
import menu_options

#########################################################################
#########################################################################
#########################################################################
# If user selects [1] Search streetinsider live -> determine top tickers -> get financial data
def run_1(master_articles, master_tickers, master_stock_data, master_ticker_reference, selections):

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
    menu_options.load_articles(master_articles, master_tickers, 'quick', selections)

    # Need to clear out non-user added top tickers
    for key, value in master_tickers.items():
        if value != 'user added':
            del master_tickers[key]

    # Determine top tickers
    menu_options.determine_top_tickers(master_articles, master_tickers, 'quick', selections)
    for key, value in master_tickers.items():
        if value != 'user added':
            selections['Tickers'].append(key)

    # Get market data for identified tickers
    menu_options.get_financial_data(master_tickers, master_stock_data, master_ticker_reference, 'quick', selections)

    # Analyze market data (do calculations) for identified tickers
    menu_options.compute_stock_metrics(master_stock_data, master_ticker_reference, 'quick', selections)

#########################################################################
#########################################################################
#########################################################################
# If user selects [2] Enter ticker(s) -> get financial data
def run_2(master_articles, master_tickers, master_stock_data, master_ticker_reference, selections):

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
    menu_options.edit_ticker_list(master_tickers, 'quick', selections)

    # Get market data for identified tickers
    menu_options.get_financial_data(master_tickers, master_stock_data, master_ticker_reference, 'quick', selections)

    # Analyze market data (do calculations) for identified tickers
    menu_options.compute_stock_metrics(master_stock_data, master_ticker_reference, 'quick', selections)

#########################################################################
#########################################################################
#########################################################################
# If user selects [3] Update stock metrics in Excel file for current day
def run_3(master_articles, master_tickers, master_stock_data, master_ticker_reference, selections):

    # Get list of available Excel files from previous computations
    available_metrics = glob2.glob('stock-data/*.xlsx')

    # Ask user which file they want to use to load articles
    prompt = '\nWhich stock metric Excel file do you want to load from?\n'
    n = 0
    for file_name in available_metrics:
        n += 1
        file_details = file_name.split('_')
        file_details.reverse()
        end_date = file_details[0][:-5]
        start_date = file_details[2]
        file_details[len(file_details)-1] = file_details[len(file_details)-1][11:]
        ticker_list = ', '.join(file_details[3:len(file_details)])
        prompt += '[{0}] Tickers: {1}\n'.format(n, ticker_list)
        if n < 10:
            space = '    '
        else:
            space = '     '
        prompt += '{0}From: {1}\tTo: {2}\n\n'.format(space, start_date, end_date)
    prompt += 'Enter number: '
    chosen_num = int(float(raw_input(prompt)))
    chosen_file = available_metrics[chosen_num-1]

    # Get the tickers in the file by parsing the chosen file name
    metrics_file = pd.ExcelFile(chosen_file)
    file_tickers = metrics_file.sheet_names

    # Get the start date of the data by parsing the chosen file name
    chosen_file_details = chosen_file.split('_')
    chosen_file_details.reverse()
    start_date = chosen_file_details[2]
    start_year = int(float(start_date.split('-')[0]))
    start_month = int(float(start_date.split('-')[1]))
    start_day = int(float(start_date.split('-')[2]))
    start = datetime.datetime(start_year, start_month, start_day)

    # Delete old Excel file
    os.remove(chosen_file)

    # Fill selections list to be passed to required functions
    selections['Quickrun'] = 3
    for ticker in file_tickers:
        selections['Tickers'].append(ticker)
    selections['Start'] = start

    # Add tickers to ticker list
    menu_options.edit_ticker_list(master_tickers, 'quick', selections)

    # Get market data for identified tickers
    menu_options.get_financial_data(master_tickers, master_stock_data, master_ticker_reference, 'quick', selections)

    # Analyze market data (do calculations) for identified tickers
    menu_options.compute_stock_metrics(master_stock_data, master_ticker_reference, 'quick', selections)

#########################################################################
#########################################################################
#########################################################################
# If user selects [4] Current test configuration (TWX from 2015-01-01 to today)
def run_4(master_articles, master_tickers, master_stock_data, master_ticker_reference, selections):

    # Fill selections list to be passed to required functions
    selections['Quickrun'] = 4
    selections['Start'] = datetime.datetime(2015, 01, 01)
    selections['Tickers'].append('TWX')

    # Add tickers to ticker list
    menu_options.edit_ticker_list(master_tickers, 'quick', selections)

    # Get market data for identified tickers
    menu_options.get_financial_data(master_tickers, master_stock_data, master_ticker_reference, 'quick', selections)

    # Analyze market data (do calculations) for identified tickers
    menu_options.compute_stock_metrics(master_stock_data, master_ticker_reference, 'quick', selections)
