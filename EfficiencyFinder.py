# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#Efficiency by Tharp
#This is a summary statistic/technical analysis tool

#Import modules
import numpy as np
import random as rand
import pandas as pd
import time as t
from DatabaseGrabber import DatabaseGrabber
from YahooGrabber import YahooGrabber

#Variable assignment
Ticker1 = 'AMD'
ATRwindow = 60
Closewindow = 60
#Request data
Asset1 = YahooGrabber(Ticker1)
Asset1 = Asset1[:] #In sample
#Calculate log returns
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
#ATR calculation
Asset1['Method1'] = Asset1['High'] - Asset1['Low']
Asset1['Method2'] = abs((Asset1['High'] - Asset1['Close'].shift(1)))
Asset1['Method3'] = abs((Asset1['Low'] - Asset1['Close'].shift(1)))
Asset1['Method1'] = Asset1['Method1'].fillna(0)
Asset1['Method2'] = Asset1['Method2'].fillna(0)
Asset1['Method3'] = Asset1['Method3'].fillna(0)
Asset1['TrueRange'] = Asset1[['Method1','Method2','Method3']].max(axis = 1)
#ATR in points; not %
Asset1['ATR'] = Asset1['TrueRange'].rolling(window = ATRwindow,
                                center=False).mean()
#Difference between n day closing prices
Asset1['CloseDiff'] = Asset1['Adj Close'] - Asset1['Adj Close'].shift(Closewindow)
#Calculate n day efficiency
Asset1['Efficiency'] = Asset1['CloseDiff'] / Asset1['ATR']
#Final metric
Efficiency = Asset1['Efficiency'][-1]
