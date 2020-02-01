# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a summary statistic tool

#Import modules 
from YahooGrabber import YahooGrabber

#Define function
def Age(s):
    #Request data
    s = YahooGrabber(s)
    #Output age
    return len(s['Adj Close'])
