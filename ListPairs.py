# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""
#This is an organizational tool that pairs items in list into a comprehensive list of all possible pairs.
#For use in SpeedDater_ apps

#Define function
def ListPairs(tickers):
    #Import modules
    import itertools as it
    #Combination object
    subList = it.combinations(tickers, 2)
    #Object to list
    fullList = list(subList)
    #Output list
    return fullList
