# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a technical analysis tool

#Import modules
from YahooGrabber import YahooGrabber
import numpy as np
from pandas_datareader import data

#Variable assignment
ticker = '^GSPC'
window = 20

#Request data
s = YahooGrabber(ticker)

#Calculate returns
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)

#Money flow multiplier calculation
s['MFMultiplier'] = (((s['Adj Close'] - s['Low']) - (s['High'] - s['Adj Close']))
                    / (s['High'] - s['Low']))
s['MFVolume'] = (s['Volume'] * s['MFMultiplier'])

#Horizontal baseline
s['ZeroLine'] = 0

#Chaikin money flow calculation
s['CMF'] = s['MFVolume'].rolling(center=False, window=window).sum(
        )/s['Volume'].rolling(center=False, window=window).sum()

#Graphical display
s[['CMF','ZeroLine']][window:].plot(grid=True, figsize=(8,3))
