# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 13:31:53 2017

@author: AmatVictoriaCuramIII
"""

#pandas_datareader is deprecated, use YahooGrabber
#This is a summary statistic tool

from pandas_datareader import data
def AverageRollingVolume(s):
    s = data.DataReader(s, 'yahoo', start='1/1/1900', end='01/01/2050')
    s['AverageRollingVolume'] = s['Volume'].rolling(center=False, 
                                                        window=252).mean()
    return s['AverageRollingVolume'].tail(1)
