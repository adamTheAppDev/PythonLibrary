# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#pandas_datareader is deprecated, use YahooGrabber
#This is a strategy tester from Yves Hilpisch's Python Finance Book

#import modules
import numpy as np
from pandas_datareader import data

#Define function
def MovingAverages(s):
    #Request data
    s = data.DataReader(s, 'yahoo', start='1/1/1900', end='01/01/2050')
    #Calculate log returns
    s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1))
    #Calculate SMA 
    s['42d'] = s['Adj Close'].rolling(window=56, center=False).mean()
    s['252d'] = s['Adj Close'].rolling(window=151, center=False).mean()
    #SMA spread
    s['42-252'] = s['42d'] - s['252d']
    #SMA spread in %
    s['Trend']= s['42-252']/s['Adj Close']
    #Directional methdology
    s['Touch'] = np.where(s['42-252'] > .039073, 1, 0)
    s['Touch'] = np.where(s['42-252'] < -.031195, -1, s['Touch'])
    s['Sustain'] = np.where(s['Touch'].shift(1) == 1, 1, 0)
    s['Sustain'] = np.where(s['Sustain'].shift(1) == 1, 1,
                                         s['Sustain'])
    s['Sustain'] = np.where(s['Touch'].shift(1) == -1, -1, 0)
    s['Sustain'] = np.where(s['Sustain'].shift(1) == -1, -1,
                                         s['Sustain'])
    s['Sustain'] = np.where(s['42-252'] > .051427, 0, s['Sustain'])
    s['Sustain'] = np.where(s['42-252'] < -.064538 , 0, s['Sustain'])
    s['Regime'] = s['Touch'] + s['Sustain']
    #Apply position to returns
    s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
    #Strategy vs underlying returns
    s[['LogRet', 'Strategy']].cumsum().apply(np.exp).plot(grid=True,
                                                    figsize=(8, 5))
    #Graphical display
    s[['42d', '252d', 'Close']].plot(grid=True, figsize=(8, 5))
    #Output strategy return stream
    return s['Strategy']
