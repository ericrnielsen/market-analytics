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

    # Print extra line
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
    aa_file_name = 'previous-runs/{0}_{1}_{2}.txt'.format(now, sites_searched_string, days_to_search)
    f = open(aa_file_name, 'w')
    f.write(str(master_articles))
    f.close()

    # End timer and print total time elapsed to live search
    end_time = time.time()
    hours, rem = divmod(end_time - start_time, 3600)
    minutes, seconds = divmod(rem, 60)
    print"\nSearch completed. Time to complete:", "{:0>2}:{:05.2f}".format(int(minutes),seconds)

    # Create string that describes the master_articles object
    file_info = aa_file_name.split('_')
    file_date = file_info[0][14:]
    file_time = ':'.join(file_info[1].split('-'))
    file_site = file_info[2]
    file_days_back = file_info[3][:-4]
    articles_description = 'Run: {0} at {1} for previous {2} days\n'.format(file_date, file_time, file_days_back)
    articles_description += 'Description: {0} articles from {1} identifying {2} total tickers'.format(len(master_articles), file_site, len(master_articles.count_tickers()))

    #########################################################################
    # Return master_articles object, description, and num_top_tickers
    return master_articles, articles_description

#########################################################################
#########################################################################
#########################################################################
# If user wants to search live
def load_previous_run():

    # Get list of available files from previous runs
    previous_runs = glob2.glob('previous-runs/*.txt')

    # Ask user which file they want to  use to load articles
    prompt = '\nWhich previous run do you want to load from?\n'
    n = 0
    for item in previous_runs:
        n += 1
        file_info = item.split('_')
        file_date = file_info[0][14:]
        file_time = ':'.join(file_info[1].split('-'))
        file_site = file_info[2]
        file_days_back = file_info[3][:-4]
        prompt += '[{0}] {1} at {2} for previous {3} days | '.format(n, file_date, file_time, file_days_back)
        prompt += 'Articles from: {0}\n'.format(file_site)
    prompt += '\nEnter number(s): '
    chosen_file = int(float(raw_input(prompt)))

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

    # Create string that describes the master_articles object
    articles_description = 'Run: {0} at {1} for previous {2} days\n'.format(file_date, file_time, file_days_back)
    articles_description += 'Description: {0} articles from {1} identifying {2} total tickers'.format(len(master_articles), file_site, len(master_articles.count_tickers()))

    #########################################################################
    # Return master_articles object and num_top_tickers
    return master_articles, articles_description
