# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 13:26:20 2017

@author: AmatVictoriaCuramIII
"""

#This is a technical analysis tool

from pandas_datareader import data
def Trend(s):# + denotes bullish, - denotes bearish
    s = data.DataReader(s, 'yahoo', start='1/1/1900', end='01/01/2050')
    s['42d'] = s['Adj Close'].rolling(window=42, center=False).mean()
    s['252d'] = s['Adj Close'].rolling(window=252, center=False).mean()
    s[['Adj Close', '42d', '252d']].plot(grid=True, figsize=(8, 5))
    s['42-252'] = s['42d'] - s['252d']
    s['Trend'] = (s['42-252']/s['Adj Close']).dropna()
    return s['Trend'].tail(1)
