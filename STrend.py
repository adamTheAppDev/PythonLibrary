# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 13:26:20 2017

@author: AmatVictoriaCuramIII
"""

#This is a technical analysis tool

def STrend(s):# + denotes bullish, - denotes bearish
    s['42d'] = s['Adj Close'].rolling(window=42, center=False).mean()
    s['252d'] = s['Adj Close'].rolling(window=252, center=False).mean()
    s['42-252'] = s['42d'] - s['252d']
    s['Trend'] = (s['42-252']/s['Adj Close']).dropna()
    return s['Trend'][-1]
