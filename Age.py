# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 13:03:32 2017

@author: AmatVictoriaCuramIII
"""

#pandas_datareader is deprecated, use YahooGrabber
#This is a time series length calculator

from pandas_datareader import data
def Age(s):
    s = data.DataReader(s, 'yahoo', start='1/1/1900', end='01/01/2050')
    return len(s['Adj Close'])
