# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#pandas_datareader is deprecated, use YahooGrabber
#This is a summary statistic tool

#Import modules 
from pandas_datareader import data # Use YahooGrabber

#Define function
def Age(s):
    #Request data - Use YahooGrabber
    s = data.DataReader(s, 'yahoo', start='1/1/1900', end='01/01/2050')
    #Output
    return len(s['Adj Close'])
