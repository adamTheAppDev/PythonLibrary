# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 13:31:53 2017

@author: AmatVictoriaCuramIII
"""

#This is a summary statistic tool

#Import modules
from YahooGrabber import YahooGrabber

#Define function - input string = 'SPY'
def AverageRollingVolume(s):
    s = YahooGrabber(s)
    #Avg rolling volume calculation 
    s['AverageRollingVolume'] = s['Volume'].rolling(center=False, 
                                                        window=252).mean()
    #Output
    return s['AverageRollingVolume'].tail(1)
