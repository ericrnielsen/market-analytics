#!/usr/bin/python

def search(num_days):

    # Import everything I need
    import os
    import objc
    import time
    import datetime
    from tqdm import tqdm
    import urllib
    import requests
    import webbrowser
    from lxml import etree
    from bs4 import BeautifulSoup
    import re
    from more_itertools import unique_everseen
    from collections import defaultdict
    from Article import Article
    from Article_List import Article_List

    # Create dictionary for all Article objects from this website
    all_articles = Article_List()

    # Create dictionary associating month numbers with month names
    months = {"01":"January", "02":"February", "03":"March",  "04":"April", \
                "05":"May", "06":"June", "07":"July",  "08":"August", \
                "09":"September", "10":"October", "11":"November",  "12":"December"}

    # Create list of dates for the past 'num_days' + 4
    dates = []
    today = datetime.datetime.today()
    temp_dates = [today - datetime.timedelta(days=x) for x in range(0, (num_days + 4))]
    for item in temp_dates:
        month = item.strftime("%B")
        day = item.strftime("%d")
        year = item.strftime("%Y")
        dates.append(month + ' ' + day + ", " + year)

    # Creat list of base URLs to search
    urls = []
    urls.append("http://www.newsoracle.com/page/")

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
        user_agent = {'User-agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=user_agent)
        html = r.content

        # Parse HTML and pull out all main inks (include article titles)
        parsed_html = BeautifulSoup(html, "lxml")
        main_links = parsed_html.find_all('h3')
        main_links = main_links[:-4]

        # If page is blank - move to next url
        if len(main_links) < 10:
            time_to_move = 0
            num_urls_searched += 1
            url_add = str(1)
            print "--------------------------"
            print "Ended on: ", url
            print "--------------------------"
            print ''
            continue

        # Pull out correct main article links
        # If an article that is 3 days old is found, set time_to_move variable to 1
        for link in main_links:
            href = link.find('a').get('href')
            cut1 = re.sub("http://www.newsoracle.com/", "", href, count = 1)
            cut2 = [cut1.split("/")[0], cut1.split("/")[1], cut1.split("/")[2]]
            if cut2[1] in months:
                date = months[cut2[1]] + " " + cut2[2] + ", " + cut2[0]
            else:
                date = "error"
                break
            # Check to see if date matches dates for last num_days
            n = 0
            while n < len(dates) - 4:
                if date == dates[n]:
                    current_article = Article()
                    current_article.set_name(link.find('a').contents[0])
                    current_article.set_href(href)
                    current_article.set_date(date)
                    all_articles.add_article(current_article)
                n += 1
            # Check to see if date is more than num_days ago
            while n < len(dates):
                if date == dates[n] and url_add != '1':
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

    # Return all_articles object
    return all_articles
