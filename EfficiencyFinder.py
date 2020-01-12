# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 13:54:45 2018

@author: AmatVictoriaCuramIII
"""

#Efficiency by Tharp
#This is a summary statistic/technical analysis tool

import numpy as np
import random as rand
import pandas as pd
import time as t
from DatabaseGrabber import DatabaseGrabber
from YahooGrabber import YahooGrabber

#Inputs - OHLC data
Ticker1 = 'AMD'
ATRwindow = 60
Closewindow = 60
Asset1 = YahooGrabber(Ticker1)
Asset1 = Asset1[:] #In
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
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
Asset1['CloseDiff'] = Asset1['Adj Close'] - Asset1['Adj Close'].shift(Closewindow)
Asset1['Efficiency'] = Asset1['CloseDiff'] / Asset1['ATR']
Efficiency = Asset1['Efficiency'][-1]
