# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a technical analysis tool

#Import modules
from pandas_datareader import data

#Define function
def Trend(s):        #Positive values denotes bullish, negative values denotes bearish
    #Request data
    s = data.DataReader(s, 'yahoo', start='1/1/1900', end='01/01/2050')
    #Calculate simple moving averages
    s['42d'] = s['Adj Close'].rolling(window=42, center=False).mean()
    s['252d'] = s['Adj Close'].rolling(window=252, center=False).mean()
    #Graphical display
    s[['Adj Close', '42d', '252d']].plot(grid=True, figsize=(8, 5))
    #SMA spread
    s['42-252'] = s['42d'] - s['252d']
    #Drop nans
    s['Trend'] = (s['42-252']/s['Adj Close']).dropna()
    #Output
    return s['Trend'].tail(1)
