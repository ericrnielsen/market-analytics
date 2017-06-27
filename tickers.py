#!/usr/bin/python

# Import everything I need
import csv

def load():

    # Read .txt file
    ticker_list = list(csv.reader(open('yahoo_usa_tickers.txt', 'rU'), delimiter='\t'))

    # Create dictionary that associates tickers with company names
    ticker_dict = {}
    for item in ticker_list:
        ticker_dict[item[0]] = item[1]

    # Test print
    #n = 1
    #for key in ticker_dict:
    #    print n, " | ", key, " ", ticker_dict[key]
    #    n += 1
    # End test print

    # Return dictionary that associates tickers with company names
    return ticker_dict

def load_refine():

    # Read .txt file
    ticker_list = list(csv.reader(open('yahoo_usa_tickers.txt', 'rU'), delimiter='\t'))

    # Create dictionary that associates tickers with company names
    ticker_dict = {}
    for item in ticker_list:
        ticker_dict[item[0]] = item[1].lower()

    # Test print 1
    #n = 1
    #for key in ticker_dict:
    #    print n, " | ", key, " ", ticker_dict[key]
    #    n += 1
    # End test print

    # Remove unnecessary chars from the end of company names
    for key in ticker_dict:
        words = ticker_dict[key].split()
        words_new = []
        for word in words:
            if word.endswith('.') or word.endswith(';') or word.endswith(',') or \
            word.endswith('\''):
                word = word[:-1]
                words_new.append(word)
            else:
                words_new.append(word)
        ticker_dict[key] = ' '.join(words_new)

    # Test print 2
    #n = 1
    #for key in ticker_dict:
    #    print n, " | ", key, " ", ticker_dict[key]
    #    n += 1
    # End test print

    # Remove unnecessary strings from company names
    for key in ticker_dict:
        words = ticker_dict[key].split()
        for word in words:
            if word == 'inc' or word == 'co' or word == 'corp' or word == 'llc' or \
            word == 'ltd' or word == 'plc' or word == 'tbk' or word == 'limited' or \
            word == 'corporation' or word == 'trust' or word == 'fund' or \
            word == 'association' or word == 'incorporated' or word == 'holdings' or \
            word == 'n.v' or word == 'co.' or word == 's.a' or word == 'group' or \
            word == 'lp' or len(word) == 1:
                words.remove(word)
        ticker_dict[key] = ' '.join(words)

    # Test print 3
    #n = 1
    #for key in ticker_dict:
    #    print n, " | ", key, " ", ticker_dict[key]
    #    n += 1
    # End test print

    return ticker_dict
