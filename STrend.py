# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a technical analysis tool

#Define function; positive values = bullish, negative values = bearish
def STrend(s):
    #Calculate simple moving averages
    s['42d'] = s['Adj Close'].rolling(window=42, center=False).mean()
    s['252d'] = s['Adj Close'].rolling(window=252, center=False).mean()
    #Difference / spread in points
    s['42-252'] = s['42d'] - s['252d']
    #In percentage terms
    s['Trend'] = (s['42-252']/s['Adj Close']).dropna()
    #Output
    return s['Trend'][-1]
