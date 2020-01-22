# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""
#pairing a list into a comprehensive list of pairs.
def ListPairs(tickers):
    import itertools as it
    subList = it.combinations(tickers, 2)
    fullList = list(subList)
    return fullList
