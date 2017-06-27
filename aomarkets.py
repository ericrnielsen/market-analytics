#!/usr/bin/python

def search(num_days):

    # Import everything I need
    import os
    import objc
    import time
    from tqdm import tqdm
    import urllib
    import urllib2
    import requests
    import webbrowser
    from lxml import etree
    from bs4 import BeautifulSoup
    import re
    from more_itertools import unique_everseen
    import operator

    # Create dictionary for counting frequency of stock tickers in article titles
    ticker_counts = {}

    # Create dictionary associating month numbers with month names
    months = {"01":"January", "02":"February", "03":"March",  "04":"April", \
                "05":"May", "06":"June", "07":"July",  "08":"August", \
                "09":"September", "10":"October", "11":"November",  "12":"December"}

    # Set current date
    dates = []
    current_month = time.strftime("%B")
    current_day = time.strftime("%d")
    current_year = time.strftime("%Y")
    dates.append(current_month + ' ' + current_day + ", " + current_year)

    # Set past num_days + 1 dates
    n = 1
    current_day_int = int(float(current_day))
    while n < (num_days + 4):
        dates.append(current_month + ' ' + str(current_day_int - n) + ", " + current_year)
        n += 1

    # Creat list of base URLs to search
    urls = []
    key_words = []
    urls.append("http://www.aomarkets.com/category/stocks/page/")
    #key_words.append("Stock Market")

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
        user_agent = {'User-agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=user_agent)
        html = r.content

        # Parse HTML and pull out all links (include article titles)
        parsed_html = BeautifulSoup(html, "lxml")
        all_links = parsed_html.find_all('a')
        # Test print
        n = 1
        for link in all_links:
            print n, ": ", link
            print ''
            n += 1
        break
        # End test print

        # Pull out main article links (assuming 9 main article links per page)
        parse1_links = []
        flag = 0
        for link in all_links:
            if flag == 1:
                parse1_links.append(link)
            elif link.contents[0] == key_words[num_urls_searched]:
                parse1_links.append(link)
                flag += 1
        parse1_links = parse1_links[:72]
        # Keep 1 link per main article
        parse2_links = []
        for link in parse1_links:
            if link.get('class') is None:
                parse2_links.append(link)
        parse3_links = []
        for link in parse2_links:
            img = link.find('img')
            if img is None:
                parse3_links.append(link)
        # Test print
        #n = 1
        #for link in parse3_links:
        #    print n, ": ", link
        #    print ""
        #    n += 1
        #break
        # End test print

        if len(parse3_links) < 9:
            time_to_move = 0
            num_urls_searched += 1
            url_add = str(1)
            print "--------------------------"
            print "Ended on: ", url
            print "--------------------------"
            print ''
            continue
        else:
            parse3_links = parse3_links[:9]
        # Test print
        #n = 1
        #for link in parse3_links:
        #    print n, ": ", link
        #    print ""
        #    n += 1
        #break
        # End test print

        # Pull out correct main article links
        # If an article that is 3 days old is found, set time_to_move variable to 1
        articles = []
        all_dates = []
        for link in parse3_links:
            href = link.get('href')
            cut1 = re.sub("http://www.zergwatch.com/", "", href, count = 1)
            cut2 = [cut1.split("/")[0], cut1.split("/")[1], cut1.split("/")[2]]
            #print cut2
            if cut2[1] in months:
                date = months[cut2[1]] + " " + cut2[2] + ", " + cut2[0]
            else:
                date = "error"
                break
            # Check to see if date matches dates for last num_days
            n = 0
            while n < len(dates) - 4:
                if date == dates[n]:
                    articles.append(link.contents[0])
                n += 1
            # Check to see if date is more than num_days ago
            while n < len(dates):
                if date == dates[n]:
                    time_to_move = 1
                n += 1
        # If nonsense date, move to next url
        if date == "error":
            time_to_move = 0
            num_urls_searched += 1
            url_add = str(1)
            print "--------------------------"
            print "Ended on: ", url
            print "--------------------------"
            print ''
            continue
        # Test print
        #for item in articles:
        #    print item
        #    print ''
        #break
        # End test print

        # Find all stock tickers (in between () in titles)
        parse1_tickers =[]
        for article in articles:
            parse1_tickers.append(re.findall('\((.*?)\)',article))
        parse2_tickers = []
        for ticker in parse1_tickers:
            for item in ticker:
                if len(item.split(":")) > 1:
                    parse2_tickers.append(str(item.split(":")[1]))
                else:
                    parse2_tickers.append(str(item))
        # Test print
        #for ticker in parse2_tickers:
        #    print ticker
        #break
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
    #return {"Test":1}
