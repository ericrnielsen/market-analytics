#!/usr/bin/python

def search(num_days):

    # Import everything I need
    import os
    #import objc
    import sys
    import time
    import datetime
    from tqdm import tqdm
    import urllib
    from requests import session
    import webbrowser
    from lxml import etree
    from bs4 import BeautifulSoup
    import re
    import www_authenticate
    from more_itertools import unique_everseen
    from collections import defaultdict
    from Article import Article
    from Article_List import Article_List
    import logging
    import platform

    # Suppress logging messages
    logging.getLogger("requests").setLevel(logging.WARNING)

    # Create dictionary for all Article objects from this website
    all_articles = Article_List()

    # Create dictionary associating month numbers with month names
    months = {"Jan":"January", "Feb":"February", "Mar":"March",  "Apr":"April", \
                "May":"May", "Jun":"June", "Jul":"July",  "Aug":"August", \
                "Sep":"September", "Oct":"October", "Nov":"November",  "Dec":"December"}

    # Create list of dates for the past 'num_days' (excluding weekends)
    dates = []
    temp_dates = []
    day_to_add = datetime.datetime.today()
    while len(temp_dates) < num_days:
        if day_to_add.weekday() < 7:
            temp_dates.append(day_to_add)
        day_to_add -= datetime.timedelta(days=1)
    for item in temp_dates:
        month = item.strftime("%B")
        day = item.strftime("%d").replace(' ', '').lstrip('0')
        year = item.strftime("%Y")
        dates.append(month + ' ' + day + ", " + year)

    # Creat list of base URLs to search
    urls = []

    # Creat list of base URLs to search
    urls = ["http://www.wsnews4investors.com/page/", \
            "http://www.wsnews4investors.com/category/technology/page/", \
            "http://www.wsnews4investors.com/category/financial/page/", \
            "http://www.wsnews4investors.com/category/health-care/page/", \
            "http://www.wsnews4investors.com/category/energy/page/", \
            "http://www.wsnews4investors.com/category/global-market/page/"]

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
    with session() as s:

        while num_urls_searched < len(urls):

            # Get HTML for the current site
            url = urls[num_urls_searched] + url_add
            r = s.get(url)
            html = r.content

            # Parse HTML and pull out all links (include article titles)
            parsed_html = BeautifulSoup(html, "lxml")
            parsed_html = parsed_html

            good_tags = parsed_html.find_all('ul', {'class':'entry-list'})
            main_content = good_tags[0].find_all('div', {'class':'entry-content'})

            ########################################################################
            ########################################################################
            ########################################################################
            # Testing here
            '''test_output = open("test.txt", "w")
            sys.stdout = test_output
            good_tags1 = parsed_html.find_all('ul', {'class':'entry-list'})
            main_content = good_tags1[0].find_all('div', {'class':'entry-content'})
            #print parsed_html.prettify().encode('ascii', 'ignore')
            #sys.exit()
            for tag in main_content:

                grab1 = tag.find('h4', {'class':'entry-title clearfix'}).find('a')
                print grab1.get('href')
                print grab1.contents[0].encode('utf-8')

                grab2 = tag.find('span', {'class':'post-date updated'}).find('a')
                print grab2.contents[0].encode('utf-8').replace(',','')

                print '\n\n'
            sys.exit()'''
            ########################################################################
            ########################################################################
            ########################################################################

            # If page is blank - move to next url
            if len(main_content) < 10:
                time_to_move = 0
                num_urls_searched += 1
                url_add = str(0)
                print "--------------------------"
                print "Ended on: ", url
                print "--------------------------"
                print ''
                continue

            # Pull out correct main article links
            # This website uses timestamps, rather than dates in urls
            # Will also need to append base url to href to get full link
            for link in main_content:
                # Get the name and href for the article
                grab1 = link.find('h4', {'class':'entry-title clearfix'}).find('a')
                # Error checking
                if len(grab1) < 1:
                    continue
                name = grab1.contents[0]#.encode('utf-8')
                href = grab1.get('href')

                # Get the date of the link
                grab2 = link.find('span', {'class':'post-date updated'}).find('a')
                date = grab2.contents[0]#.encode('utf-8')

                # Get the time of the link
                time = "None"

                # Check to see if date matches dates for last num_days
                # If so, add article to all_articles object
                n = 0
                date_match = False
                while n < len(dates):
                    #print date
                    #print dates[n]
                    #print ''
                    if date == dates[n]:
                        date_match = True
                        current_article = Article()
                        current_article.set_name(name)
                        current_article.set_href(href)
                        current_article.set_date(date)
                        current_article.set_time(time)
                        all_articles.add_article(current_article)
                        break
                    n += 1
                # Check to see if date is more than num_days ago
                # If date not matched, time to move to next site
                if date_match == False:
                    time_to_move = 1

            # If an article that is 3 days old has been found, move to next base URL
            # Else increment url_add to move to next page on current base URL
            if time_to_move == 1:
                time_to_move = 0
                num_urls_searched += 1
                # Conditional set needed for financial category (due to strange website)
                if (num_urls_searched == 2):
                    url_add = str(10)
                else:
                    url_add = str(0)
                print "--------------------------"
                print '{0}/{1} Ended on: {2}'.format(num_urls_searched, len(urls), url)
                print ''
                #sys.stdout.write("\rSearched %s of 1 pages" % num_urls_searched)
                #sys.stdout.flush()
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

    return all_articles
