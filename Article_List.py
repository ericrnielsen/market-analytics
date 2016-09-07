#!/usr/bin/python

import operator
import Article
import json

class Article_List:

    def __init__(self):
        self.articles = []

    def __len__(self):
        return len(self.articles)

    def __str__(self):
        to_return = ''
        for article in self.articles:
            to_return += str(article)
            to_return += '\n'
        return to_return

    def exists(self, article):
        index = -1
        for item in self.articles:
            index += 1
            if article == item:
                return index
        # If nothing matched, return None
        return None

    def add_article(self, article):
        index = self.exists(article)
        if index is None:
            self.articles.append(article)
            return 1
        else:
            return None

    def get_article(self, article):
        index = self.exists(article)
        if index is not None:
            return self.article[index]
        else:
            return None

    def edit_article(self, article, edit_type, value):
        to_edit = self.get_article(article)
        if to_edit is not None:
            if edit_type == "name":
                to_edit.set_name(value)
                return 1
            if edit_type == "href":
                to_edit.set_href(value)
                return 1
            if edit_type == "date":
                to_edit.set_date(value)
                return 1
            if edit_type == "tickers":
                to_edit.add_tickers(value)
                return 1
            if edit_type == "keywords":
                to_edit.add_keywords(value)
                return 1
            else:
                return None
        else:
            return None

    def count_tickers(self):
        counts = {}
        for article in self.articles:
            for item in article.tickers:
                if item in counts:
                    counts[item] += 1
                else:
                    counts[item] = 1
        return counts

    def return_top(self, top_num):
        counts = self.count_tickers()
        sorted_counts = sorted(counts.items(), key=operator.itemgetter(1))
        sorted_counts.reverse()
        return sorted_counts[:top_num]

    def all_for_ticker(self, ticker):
        to_return = Article_List()
        for article in self.articles:
            for item in article.tickers:
                if item == ticker:
                    to_return.add_article(article)
                    continue
        return to_return

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
