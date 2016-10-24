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

#########################################################################
#########################################################################
#########################################################################
# If user wants to search live
def load_live():

    # Start timer
    start_time = time.time()

    # Ask user what sites they want to search
    prompt = '\nWhich site(s) do you want to search?\n[1] zergwatch\n[2] streetupdates' + \
    '\n[3] newsoracle\n[4] smarteranalyst\n[5] streetinsider !!\n\nEnter number(s): '
    response_list = raw_input(prompt).split(' ')

    # Have user input number of days worth of articles they want to search
    print ''
    var = raw_input("How many days back do you want to search? ")
    days_to_search = int(float(var))

    # Have user input number of top tickers they're interested in for the run
    print ''
    var = raw_input("How many top tickers do you want to learn about? ")
    num_top_tickers = int(float(var))
    print ''

    # Create master tickers list
    master_articles = Article_List()
    sites_searched = []

    #########################################################################
    # Search zergwatch.com and get all articles within past 'days_to_search'
    if '1' in response_list:
        sites_searched.append('zergwatch')
        zergwatch_articles = zergwatch.search(days_to_search)
    else:
        zergwatch_articles = Article_List()

    #########################################################################
    # Search streetupdates.com and get all articles within past 'days_to_search'
    if '2' in response_list:
        sites_searched.append('streetupdates')
        streetupdates_articles = streetupdates.search(days_to_search)
    else:
        streetupdates_articles = Article_List()

    #########################################################################
    # Search newsoracle.com and get all articles within past 'days_to_search'
    if '3' in response_list:
        sites_searched.append('newsoracle')
        newsoracle_articles = newsoracle.search(days_to_search)
    else:
        newsoracle_articles = Article_List()

    #########################################################################
    # Search smarteranalyst.com and get all articles within past 'days_to_search'
    if '4' in response_list:
        sites_searched.append('smarteranalyst')
        smarteranalyst_articles = smarteranalyst.search(days_to_search)
    else:
        smarteranalyst_articles = Article_List()

    #########################################################################
    # Search streetinsider.com and get all articles within past 'days_to_search'
    if '5' in response_list:
        sites_searched.append('streetinsider')
        streetinsider_articles = streetinsider.search(days_to_search)
    else:
        streetinsider_articles = Article_List()

    #########################################################################
    # Add all returned articles to master Article_List object
    for article in zergwatch_articles.articles:
        master_articles.add_article(article)
    for article in streetupdates_articles.articles:
        master_articles.add_article(article)
    for article in newsoracle_articles.articles:
        master_articles.add_article(article)
    for article in smarteranalyst_articles.articles:
        master_articles.add_article(article)
    for article in streetinsider_articles.articles:
        master_articles.add_article(article)

    #########################################################################
    # Save all articles to a file for later reference
    sites_searched_string = "_".join(sites_searched)
    format = "%m-%d-%Y_%H-%M-%S"
    now = datetime.datetime.today().strftime(format)
    file_name = 'previous-runs/all-articles/{0}_{1}_{2}_{3}_aa.txt'.format(now, sites_searched_string, days_to_search, num_top_tickers)
    f = open(file_name, 'w')
    f.write(str(master_articles))
    f.close()

    #########################################################################
    # Save articles for just top tickers for later reference
    num_total_tickers = len(master_articles.count_tickers())
    top_tickers = master_articles.return_top(num_top_tickers)
    n = 0
    file_name = 'previous-runs/top-tickers/{0}_{1}_{2}_{3}_tt.txt'.format(now, sites_searched_string, days_to_search, num_top_tickers)
    with open(file_name, 'w') as f2:
        sys.stdout = f2
        print 'Top {0} most common tickers:'.format(str(num_top_tickers))
        for item in top_tickers:
            print '{0}:\t{1}'.format(item[0], item[1])
        for item in top_tickers:
            n += 1
            print '\n-----------------------------------------------------------'
            print '[#{0} / {1} total tickers] {2}'.format(n, num_total_tickers, item[0])
            print '-----------------------------------------------------------\n'
            #print '-----------------------------'
            #print 'Stock info for {0} at {1}'.format(item[0], str(datetime.datetime.now()))
            #print '-----------------------------'
            #stock_info = Current_StockInfo(item[0])
            #print stock_info
            print '-----------------------------'
            print 'All {0} articles for {1}'.format(item[1], item[0])
            print '-----------------------------'
            print master_articles.all_for_ticker(item[0])
    f2.close()
    sys.stdout = sys.__stdout__

    # End timer and print total time elapsed to live search
    end_time = time.time()
    hours, rem = divmod(end_time - start_time, 3600)
    minutes, seconds = divmod(rem, 60)
    print"\nSearch completed. Time to complete:", "{:0>2}:{:05.2f}".format(int(minutes),seconds)

    #########################################################################
    # Return master_articles object and num_top_tickers
    return master_articles, num_top_tickers

#########################################################################
#########################################################################
#########################################################################
# If user wants to search live
def load_previous_run():

    # Get list of available files from previous runs
    previous_runs = glob2.glob('previous-runs/all-articles/*.txt')

    # Ask user which file they want to  use to load articles
    prompt = '\nWhich previous run do you want to load from?\n'
    n = 0
    for item in previous_runs:
        n += 1
        file_info = item.split('_')
        file_date = file_info[0][27:]
        file_time = ':'.join(file_info[1].split('-'))
        file_site = file_info[2]
        file_days_back = file_info[3]
        file_num_top =  file_info[4]
        prompt += '[{0}] {1} at {2} | '.format(n, file_date, file_time)
        prompt += 'Articles for {0} days from: {1} | '.format(file_days_back, file_site)
        prompt += 'IDd {0} top tickers\n'.format(file_num_top)
    prompt += '\nEnter number(s): '
    chosen_file = int(float(raw_input(prompt)))

    # Set num_top_tickers variable for later use
    num_top_tickers = int(float(previous_runs[chosen_file-1].split('_')[4]))

    # Read from selected file and load master_articles object
    master_articles = Article_List()
    with open(previous_runs[chosen_file-1], 'r') as load_file:
        content = load_file.readlines()
        n = 0
        # Loop through each line in the file, look at 5 lines at a time
        while n < len(content):
            # Make new article object
            current_article = Article()
            # Get and set article name
            name = content[n][9:].rstrip()
            current_article.set_name(name)
            n += 1
            # Get article href
            href = content[n][9:].rstrip()
            current_article.set_href(href)
            n += 1
            # Get article date
            date = content[n][9:].rstrip()
            current_article.set_date(date)
            n += 3
            # Add article to master article list
            master_articles.add_article(current_article)
    load_file.close()

    #########################################################################
    # Return master_articles object and num_top_tickers
    return master_articles, num_top_tickers

#########################################################################
#########################################################################
#########################################################################
# Printing out info about identified top tickers
def display_top_tickers(master_articles, num_top_tickers):
    num_total_tickers = len(master_articles.count_tickers())
    top_tickers = master_articles.return_top(num_top_tickers)
    n = 0
    print '\nTop {0} most common tickers:'.format(str(num_top_tickers))
    for item in top_tickers:
        print '{0}:\t{1}'.format(item[0], item[1])
    for item in top_tickers:
        n += 1
        print '\n-----------------------------------------------------------'
        print '[#{0} / {1} total tickers] {2}'.format(n, num_total_tickers, item[0])
        print '-----------------------------------------------------------\n'
        print '-----------------------------'
        print 'All {0} articles for {1}'.format(item[1], item[0])
        print '-----------------------------'
        print master_articles.all_for_ticker(item[0])
