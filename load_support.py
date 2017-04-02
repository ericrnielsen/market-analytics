#!/usr/bin/python

import sys
import operator
import time
import datetime
from Article import Article
from Article_List import Article_List
import zergwatch
import streetupdates
import newsoracle
import smarteranalyst
import streetinsider
import wsnews4investors
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
def load_live(master_articles, run_type, selections):

    # Start timer
    start_time = time.time()

    # If need to get user input manually (not a quick run)
    if run_type == 'manual':
        ######################################################
        # Ask user what sites they want to search (in loop until valid selection)
        valid = False
        while valid == False:
            prompt = '\nWhich site(s) do you want to search?\n' + \
            '[1] streetinsider\n' + \
            '[2] wsnews4investors\n\n' + \
            'Enter number(s): '
            response_list = raw_input(prompt).split(' ')
            try:
                response_list = [int(float(num)) for num in response_list]
                # This isn't the best way to check validity, but will be good
                # if we add more sites
                valid = all(num in range(1,3) for num in response_list)
                response_list = [str(num) for num in response_list]
            except KeyboardInterrupt:
                print'\n'
                sys.exit()
            except:
                pass
            if valid == False:
                print '\nInvalid selection. Please try again.'
        # End selection loop
        ######################################################

        # Have user input number of days worth of articles they want to search
        print ''
        var = raw_input("How many days back do you want to search? ")
        days_to_search = int(float(var))

    # Else it's a quick run so user inputs already entered
    else:
        response_list = '1'
        days_to_search = selections['Days to Search']

    # Print extra line
    print ''

    # Create master tickers list
    master_articles_new = Article_List()
    sites_searched = []

    #########################################################################
    # Search streetinsider.com and get all articles within past 'days_to_search'
    if '1' in response_list:
        sites_searched.append('streetinsider')
        streetinsider_articles = streetinsider.search(days_to_search)
        # Add all returned articles to master Article_List object
        for article in streetinsider_articles.articles:
            master_articles_new.add_article(article)
    else:
        streetinsider_articles = Article_List()

    #########################################################################
    # Search wsnews4investors.com and get all articles within past 'days_to_search'
    if '2' in response_list:
        sites_searched.append('wsnews4investors')
        wsnews4investors_articles = wsnews4investors.search(days_to_search)
        # Add all returned articles to master Article_List object
        for article in wsnews4investors_articles.articles:
            master_articles_new.add_article(article)
    else:
        wsnews4investors_articles = Article_List()

    #########################################################################
    # Save all articles to a file for later reference
    sites_searched_string = "_".join(sites_searched)
    format = "%m-%d-%Y_%H-%M-%S"
    now = datetime.datetime.today().strftime(format)
    aa_file_name = 'previous-runs/{0}_{1}_{2}.txt'.format(now, sites_searched_string, days_to_search)
    f = open(aa_file_name, 'w')
    f.write(str(master_articles_new))
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
    articles_description += 'Description: {0} articles from {1} identifying {2} total tickers'.format(len(master_articles_new), file_site, len(master_articles_new.count_tickers()))
    master_articles_new.add_description(articles_description)

    #########################################################################
    # Reset master_articles object with the contents of master_articles_new
    master_articles.reset(master_articles_new)

#########################################################################
#########################################################################
#########################################################################
# If user wants to search live
def load_previous_run(master_articles):

    # Get list of available files from previous runs
    previous_runs = glob2.glob('previous-runs/*.txt')

    ######################################################
    # Ask user which file they want to  use to load articles (in loop until valid selection)
    valid = False
    while valid == False:
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
        try:
            choice = int(float(raw_input(prompt)))
        except KeyboardInterrupt:
            print'\n'
            sys.exit()
        except:
            choice = -1
        if choice in range(1,n+1):
            valid = True
        if valid == False:
            print '\nInvalid selection. Please try again.'
    # End selection loop
    ######################################################

    # Read from selected file and load master_articles object
    master_articles_new = Article_List()
    with open(previous_runs[choice-1], 'r') as load_file:
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
            master_articles_new.add_article(current_article)
    load_file.close()

    # Create string that describes the master_articles object
    articles_description = 'Run: {0} at {1} for previous {2} days\n'.format(file_date, file_time, file_days_back)
    articles_description += 'Description: {0} articles from {1} identifying {2} total tickers'.format(len(master_articles_new), file_site, len(master_articles_new.count_tickers()))
    master_articles_new.add_description(articles_description)

    #########################################################################
    # Reset master_articles object with the contents of master_articles_new
    master_articles.reset(master_articles_new)
