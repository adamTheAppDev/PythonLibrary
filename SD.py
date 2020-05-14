# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a summary statistic + database query tool

#Import modules
import numpy as np
from pandas_datareader import data

#Define function
def SD(s):
    #Request data
    s = data.DataReader(s, 'yahoo', start='1/1/1900', end='01/01/2050')
    #Calculate log returns
    s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1))
    #Calculate standard deviation
    s['SD'] = np.std(s['LogRet'])*np.sqrt(252)
    #Output
    return s['SD'].tail(1)
