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
        if day_to_add.weekday() < 5:
            temp_dates.append(day_to_add)
        day_to_add -= datetime.timedelta(days=1)
    for item in temp_dates:
        month = item.strftime("%B")
        day = item.strftime("%d").replace(' ', '')
        year = item.strftime("%Y")
        dates.append(month + ' ' + day + ", " + year)

    # Creat list of base URLs to search
    urls = []
    # Company News
    urls.append("http://www.streetinsider.com/Corporate+News?offset=")
    urls.append("http://www.streetinsider.com/Hot+Corp.+News?offset=")
    urls.append("http://www.streetinsider.com/Litigation?offset=")
    urls.append("http://www.streetinsider.com/Management+Changes?offset=")
    urls.append("http://www.streetinsider.com/Hot+Mgmt+Changes?offset=")
    urls.append("http://www.streetinsider.com/Management+Comments?offset=")
    urls.append("http://www.streetinsider.com/Retail+Sales?offset=")

    # Dividends/Sh
    urls.append("http://www.streetinsider.com/Dividends?offset=")
    urls.append("http://www.streetinsider.com/Hot+Dividends?offset=")
    urls.append("http://www.streetinsider.com/Dividend+Hike?offset=")
    urls.append("http://www.streetinsider.com/Special+Dividends?offset=")
    urls.append("http://www.streetinsider.com/Stock+Buybacks?offset=")
    urls.append("http://www.streetinsider.com/Hot+Buybacks?offset=")
    urls.append("http://www.streetinsider.com/Stock+Splits?offset=")

    # EPS
    urls.append("http://www.streetinsider.com/Conference+Calls?offset=")
    urls.append("http://www.streetinsider.com/Earnings?offset=")
    urls.append("http://www.streetinsider.com/Hot+Earnings?offset=")
    urls.append("http://www.streetinsider.com/Guidance?offset=")
    urls.append("http://www.streetinsider.com/Hot+Guidance?offset=")

    # ETFs
    urls.append("http://www.streetinsider.com/ETFs?offset=")

    # FDA
    urls.append("http://www.streetinsider.com/FDA?offset=")
    urls.append("http://www.streetinsider.com/Hot+FDA+News?offset=")

    # Insiders/Hedge Funds
    urls.append("http://www.streetinsider.com/13Ds?offset=")
    urls.append("http://www.streetinsider.com/13Fs?offset=")
    urls.append("http://www.streetinsider.com/13Gs?offset=")
    urls.append("http://www.streetinsider.com/Hedge+Funds?offset=")

    urls.append("http://www.streetinsider.com/Hot+Hedge+Fund+News?offset=")
    urls.append("http://www.streetinsider.com/Insider+Trades?offset=")
    urls.append("http://www.streetinsider.com/Hot+Insider+Trades?offset=")

    # M&A
    urls.append("http://www.streetinsider.com/Mergers+and+Acquisitions?offset=")
    urls.append("http://www.streetinsider.com/Hot+M+and+A?offset=")
    urls.append("http://www.streetinsider.com/Private+Equity?offset=")
    urls.append("http://www.streetinsider.com/Rumors?offset=")
    urls.append("http://www.streetinsider.com/Spinoffs?offset=")

    # Market Movers
    urls.append("http://www.streetinsider.com/Hot+List?offset=")
    urls.append("http://www.streetinsider.com/Index+Changes?offset=")
    urls.append("http://www.streetinsider.com/Insiders+Blog?offset=")
    urls.append("http://www.streetinsider.com/Momentum+Movers?offset=")
    urls.append("http://www.streetinsider.com/Options?offset=")
    urls.append("http://www.streetinsider.com/Option+EPS+Action?offset=")
    urls.append("http://www.streetinsider.com/Short+Sales?offset=")
    urls.append("http://www.streetinsider.com/Special+Reports?offset=")
    urls.append("http://www.streetinsider.com/Technicals?offset=")
    urls.append("http://www.streetinsider.com/Trading+Halts?offset=")
    urls.append("http://www.streetinsider.com/Trader+Talk?offset=")

    # Offerings
    urls.append("http://www.streetinsider.com/Equity+Offerings?offset=")
    urls.append("http://www.streetinsider.com/IPOs?offset=")
    urls.append("http://www.streetinsider.com/Hot+IPOs?offset=")

    # Other
    urls.append("http://www.streetinsider.com/Contributors?offset=")
    urls.append("http://www.streetinsider.com/General+News?offset=")

    # Rating Changes
    urls.append("http://www.streetinsider.com/Analyst+Comments?offset=")
    urls.append("http://www.streetinsider.com/Hot+Comments?offset=")
    urls.append("http://www.streetinsider.com/Analyst+EPS+Change?offset=")
    urls.append("http://www.streetinsider.com/Analyst+EPS+View?offset=")
    urls.append("http://www.streetinsider.com/Analyst+PT+Change?offset=")
    urls.append("http://www.streetinsider.com/Credit+Ratings?offset=")
    urls.append("http://www.streetinsider.com/Downgrades?offset=")
    urls.append("http://www.streetinsider.com/Hot+Downgrades?offset=")
    urls.append("http://www.streetinsider.com/New+Coverage?offset=")
    urls.append("http://www.streetinsider.com/Hot+New+Coverage?offset=")
    urls.append("http://www.streetinsider.com/Upgrades?offset=")
    urls.append("http://www.streetinsider.com/Hot+Upgrades?offset=")

    # Set num_url_searched variable to 0
    # Set time_to_move (to next base URL) variable to 0
    num_urls_searched = 0
    time_to_move = 0

    # Create url extention variable (will increment to move through website pages)
    url_add = str(0)

    #########################################################################
    #
    # Initiate session with streetinsider
    # Login and confirm that it succeeded
    # Then do everything else in the article search within that session
    #
    #########################################################################

    # Determine correct file path for local file with authentication information
    # Three options - Justin's computer, Eric's computer, or Kyle's computer
    if platform.uname()[1] == 'DESKTOP-641I540':
        file_name = "C:\Users\Justin\Desktop\stock_project\street-insider-auth/streetinsiderauth.txt"
    elif platform.uname()[1] == 'Erics-MacBook-Pro.local':
        file_name = os.path.expanduser("~/Desktop/street-insider-auth/streetinsiderauth.txt")
    else:
        file_name = os.path.expanduser("~/Desktop/street-insider-auth/streetinsiderauth.txt")

    # Get StreetInsider Premium authentication information from local file
    f = open(file_name, 'r')
    lines = f.readlines()
    login_payload = {}
    login_payload[lines[0].rstrip("\n")] = lines[1].rstrip("\n")
    login_payload[lines[2].rstrip("\n")] = lines[3].rstrip("\n")
    login_payload[lines[4].rstrip("\n")] = lines[5].rstrip("\n")
    login_payload[lines[6].rstrip("\n")] = lines[7].rstrip("\n")
    login_payload[lines[8].rstrip("\n")] = lines[9].rstrip("\n")
    remove_duplicate_payload = {}
    remove_duplicate_payload[lines[10].rstrip("\n")] = lines[11].rstrip("\n")
    headers = {}
    headers[lines[12].rstrip("\n")] = lines[13].rstrip("\n")

    # Initiate session and login into website
    with session() as s:

        # Check to see if already logged into StreetInsider Premium
        logged_in = False
        s.headers = headers
        check1_source = s.get('https://www.streetinsider.com/account_home.php')
        check1_html = BeautifulSoup(check1_source.content, "lxml")
        if not check1_html.find_all("h1")[0].contents[0] == 'Member Login':
            logged_in = True

        # If not already logged in, log in
        if logged_in == False:
            # Login with credentials
            r1 = s.post('https://www.streetinsider.com/login.php', data=login_payload)

            # If login results takes you to 'Duplicate Login' page, end the prior session
            r1_parsed = BeautifulSoup(r1.content, "lxml")
            h1_tags = r1_parsed.find_all("h1")
            if h1_tags[0].contents[0] == 'Duplicate Login':
                r2 = s.post(r1.url, data=remove_duplicate_payload)

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
            url = urls[num_urls_searched] + url_add
            r = s.get(url)
            html = r.content

            # Parse HTML and pull out all links (include article titles)
            parsed_html = BeautifulSoup(html, "lxml")
            good_tags1 = parsed_html.find_all('dl', {'class':'news_list'})
            main_links = good_tags1[0].find_all('dt')

            # If on the first page of a site, there are 5 extra articles at the top
            if url_add == str(0):
                good_tags2 = parsed_html.find_all('div', {'class':'news_article'})
                index = 0
                for tag in good_tags2:
                    main_links.insert(index,tag)
                    index += 1

            # If page is blank - move to next url
            if len(main_links) < 5:
                time_to_move = 0
                num_urls_searched += 1
                url_add = str(0)
                print "--------------------------"
                print "Ended on: ", url
                print "--------------------------"
                print ''
                continue

            # Pull out correct main article links
            # If an article that is 3 days old is found, set time_to_move variable to 1
            # This website uses timestamps, rather than dates in urls
            # Will also need to append base url to href to get full link
            for link in main_links:
                # Get the name and href for the article
                a_tag = link.find('a', {'class':['news_title', 'story_title']})
                # Error checking
                if len(a_tag) < 1:
                    continue
                name = a_tag.contents[0]
                href = a_tag.get('href')

                # Get the date of the link
                date = link.find('span', {'class':'timestamp'}).contents[0]

                # Get the time of the link
                time = date.split(" ")[3]

                # Months in dates only have 3 chars, so need to standardize to full month names
                date_month = date.split(" ")[0]
                date_day = date.split(" ")[1]
                date_year = date.split(" ")[2]
                if date_month in months:
                    date = months[date_month] + " " + date_day + " " + date_year
                else:
                    date = "error"
                    break

                # Check to see if date matches dates for last num_days
                # If so, add article to all_articles object
                n = 0
                date_match = False
                while n < len(dates):
                    if date == dates[n]:
                        date_match = True
                        current_article = Article()
                        current_article.set_name(name)
                        current_article.set_href(href)
                        current_article.set_date(date)
                        current_article.set_time(time)
                        all_articles.add_article(current_article)
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
                url_add = str(0)
                #print "--------------------------"
                #print '{0}/{1} Ended on: {2}'.format(num_urls_searched, len(urls), url)
                #print ''
                sys.stdout.write("\rSearched %s of 62 pages" % num_urls_searched)
                sys.stdout.flush()
            else:
                #print "Just searched: ", url
                url_add_int = int(float(url_add))
                url_add_int += 50
                url_add = str(url_add_int)

        #########################################################################
        #
        # Outside of the while loop (all pages with articles < 3 days old viewed)
        #
        #########################################################################

        # Log out of StreetInsider Premium
        logout = s.get('http://www.streetinsider.com/login.php?logout=true')
        logout_html = BeautifulSoup(logout.content, "lxml")

    # Return all_articles object
    return all_articles
