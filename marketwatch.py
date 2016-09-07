#!/usr/bin/python

def search(num_days):

    # Import everything I need
    import os
    import objc
    import time
    from tqdm import tqdm
    import urllib
    import requests
    import webbrowser
    from lxml import etree
    from bs4 import BeautifulSoup
    import re
    from more_itertools import unique_everseen
    import operator

    # Create dictionary for counting frequency of stock tickers in article titles
    ticker_counts = {}

    # Set current date
    dates = []
    current_month = time.strftime("%B")
    current_day = time.strftime("%d")
    current_year = time.strftime("%Y")
    dates.append(current_month + ' ' + current_day + ", " + current_year)

    # Set past num_days + 1 dates
    n = 1
    current_day_int = int(float(current_day))
    while n < (num_days + 2):
        dates.append(current_month + ' ' + str(current_day_int - n) + ", " + current_year)
        n += 1

    # Creat list of base URLs to search
    urls = ["http://www.zergwatch.com/category/wall-street-coverage/page/", \
            "http://www.zergwatch.com/category/analyst-opinions/page/", \
            "http://www.zergwatch.com/category/worldmarkets2016/page/", \
            "http://www.zergwatch.com/category/earning-estimates/page/"]

    # Set num_url_searched variable to 0
    # Set time_to_move (to next base URL) variable to 0
    num_urls_searched = 0
    time_to_move = 0

    # Create url extention variable (will increment to move through website pages)
    url_add = str(1)

    #########################################################################
    #
    # Pull and parse website pages for base URL until 3 day-old articles reached
    # Then num_urls_searched will be increased by 1 and a new base URL will be searched
    # Continue until all articles < 3 days old on all base URL are gathered
    # Will eventually need to modify to consider end of months
    #
    #########################################################################
    while num_urls_searched < len(urls):
        # Get HTML for the current site
        url = urls[num_urls_searched] + url_add + "/"
        # Test print
        #print "---------------------"
        #print "url: ", url
        #print "---------------------"
        # End test print
        html = urllib.urlopen(url)

        # Parse HTML and pull out all links (include article titles)
        parsed_html = BeautifulSoup(html, "lxml")
        all_links = parsed_html.find_all('a')

        #all_articles = [article.get('title') for article in parsed_html.find_all('a')]

        # Pull out article links
        parse1_links = []
        for link in all_links:
            if link.get('title') and 'Permalink' in link.get('title'):
                parse1_links.append(link)
        # Test print
        #for link in parse1_links:
        #    print link.get('title')
        #    print ""
        #break
        # End test print

        # Pull out main article links
        parse2_links = []
        for link in parse1_links:
            if 'NASDAQ:' not in link.get('title') and \
            'NYSE:' not in link.get('title') and \
            'NYSEMKT:' not in link.get('title') and \
            'LON:' not in link.get('title'):
                parse2_links.append(link)
        # Test print
        #for link in parse2_links:
        #   print link.get('title')
        #   print ''
        #   print link.contents
        #   print ''
        #   print ''
        # End test print

        # Pull out correct main article links
        # Remove first 6 because those are the same on all pages (cause TBD)
        # If an article that is 3 days old is found, set time_to_move variable to 1
        parse3_links = []
        all_dates = []
        for link in parse2_links:
            date = link.contents[0]

            # Check to see if date matches dates for last num_days
            n = 0
            while n < len(dates) - 2:
                if date == dates[n]:
                    parse3_links.append(link)
                n += 1
            # Check to see if date is more than num_days ago
            while n < len(dates):
                if date == dates[n]:
                    time_to_move = 1
                n += 1
            #if date == dates[0] or date == current_date_minus1 or date == current_date_minus2:
            #    parse3_links.append(link)
            #elif date == current_date_minus3 or date == current_date_minus4:
            #    time_to_move = 1
        parse3_links = parse3_links[6:]
        # Test print
        #for item in parse3_links:
        #    print item.get('title')
        #    print item.contents
        #    print ''
        # End test print

        # Build dictionary associating article titles with article dates
        articles = {}
        article_title = ""
        article_date = ""
        for link in parse3_links:
            article_title = link.get('title')
            article_title = re.sub("Permalink to ", "", article_title, count = 1)
            article_date = link.contents[0]
            article_date = re.sub("u\'", "", article_date, count = 1)
            article_date = re.sub("\'", "", article_date, count = 1)
            articles[article_title] = article_date
        # Test print
        #for article in articles:
        #    print article, " : ", articles[article]
        # End test print

        # Find all stock tickers (in between () in titles)
        parse1_tickers =[]
        for article in articles:
            parse1_tickers.append(re.findall('\((.*?)\)',article))
        # Test print
        #for ticker in parse1_tickers:
        #    print ticker
        # End test print

        # Get unique strings for all tickers (because re.findall returns lists)
        parse2_tickers = []
        for ticker in parse1_tickers:
            for item in ticker:
                parse2_tickers.append(item)
        # Test print
        #for ticker in parse2_tickers:
        #    print ticker
        # End test print

        # If ticker already in dictionary (has already been seen in past 2 days), then
        # increase ticker count in dictionary
        # If ticker not already in dictionary (has not been seen in the past 2 days), then
        # add ticker to the dictionary and set count to 1
        for ticker in parse2_tickers:
            if ticker in ticker_counts:
                ticker_counts[ticker] += 1
            else:
                ticker_counts[ticker] = 1
        # Test print
        #for ticker in ticker_counts:
        #    print ticker, " : ", ticker_counts[ticker]
        # End test print

        # Test print
        #print ""
        #print "--------------------------"
        #print "--------------------------"
        #print""
        # End test print

        # If an article that is 3 days old has been found, move to next base URL
        # Else increment url_add to move to next page on current base URL
        if time_to_move == 1:
            time_to_move = 0
            num_urls_searched += 1
            url_add = str(1)
            print "--------------------------"
            print "Ended on: ", url
            print "--------------------------"
            print ''
        else:
            print "Just searched: ", url
            url_add_int = int(float(url_add))
            url_add_int += 1
            url_add = str(url_add_int)

    #########################################################################
    #
    # Outside of the while loop (all pages with articles < 3 days old viewed)
    #
    #########################################################################

    return ticker_counts
