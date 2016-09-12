#!/usr/bin/python

from yahoo_finance import Share
import StockInfo

class Article_List:

    def __init__(self):
        self.stat_sets = []

    def __len__(self):
        return len(self.stat_sets)

    def __str__(self):
        to_return = ''
        for item in self.stat_sets:
            to_return += str(item)
            to_return += '\n'
        return to_return

    def exists(self, to_compare):
        index = -1
        for item in self.stat_sets:
            index += 1
            if to_compare.get_name() == item.get_name():
                return index
        # If nothing matched, return None
        return None

    def add_stat_set(self, to_add):
        index = self.exists(to_add)
        if index is None:
            self.stat_sets.append(to_add)
            return 1
        else:
            return None

    # TBD if this will actually be used, so not adding any additional functions for now        
