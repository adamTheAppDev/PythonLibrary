# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""
#This is an organizational tool that pairs items in list into a comprehensive list of all possible pairs.
#For use in SpeedDater_ apps

def ListPairs(tickers):
    import itertools as it
    subList = it.combinations(tickers, 2)
    fullList = list(subList)
    return fullList
