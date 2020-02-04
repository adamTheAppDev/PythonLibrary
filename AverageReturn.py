# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#Use YahooGrabber for data req
#This is a summary statistic tool

#Import modules
import numpy as np
from DatabaseGrabber import DatabaseGrabber

#Define function
def AverageReturn(s):
    #Request data
    s = DatabaseGrabber(s)
    #Calculate log returns
    s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1))
    #Calculate avg returns
    s['Mean'] = np.mean(s['LogRet'])*252
    #Output
    return s['Mean'].tail(1)
