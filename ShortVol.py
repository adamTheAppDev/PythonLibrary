# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 23:23:57 2017

@author: AmatVictoriaCuramIII
"""
import numpy as np
from pandas_datareader import data
s = data.DataReader('^VIX', 'yahoo', start='1/1/1900', end='01/01/2050') 
s2 = data.DataReader('^VXV', 'yahoo', start='1/1/1900', end='01/01/2050') 
s3 = data.DataReader('VXX', 'yahoo', start='1/1/1900', end='01/01/2050')
def ShortVol(x, y):
    s3['LogRet'] = np.log(s3['Adj Close']/s3['Adj Close'].shift(1))
    s3['LogRet'] = s3['LogRet'].fillna(0)
    s3['Meter'] = s['Close']/s2['Close']
    s3['Meter'].plot(grid=True, figsize=(8, 5))
    s3['Touch'] = np.where(s3['Meter'] < x, -1, 0) # short signal
    s3['Touch'] = np.where(s3['Meter'] > y, 0, s3['Touch']) #flat signal
    s3['Sustain'] = np.where(s3['Touch'].shift(1) == -1, -1, 0) #short
    s3['Sustain'] = np.where(s3['Sustain'].shift(1) == -1, -1, #stays
                                         s3['Sustain']) #short
    s3['Sustain'] = np.where(s3['Touch'].shift(1) == 0, 0, 0) #flat
    s3['Sustain'] = np.where(s3['Sustain'].shift(1) == 0, 0, #stays
                                         s3['Sustain']) #flat
#    s3['Sustain'] = np.where(s3['Meter'] < .8, 0, s3['Sustain']) #cover short
    s3['Regime'] = s3['Touch'] + s3['Sustain']
    s3['Strategy'] = (s3['Regime']).shift(1)*s3['LogRet']
    s3['Strategy'] = s3['Strategy'].fillna(0)
    endgains = 1
    endreturns = 1
    returnstream = []
    gainstream = []
    for i in s3['LogRet']:
        slate = endreturns * (1+-i)
        returnstream.append(slate)
        endreturns = slate
    for i in s3['Strategy']:
        otherslate = endgains * (1+i)
        gainstream.append(otherslate)
        endgains = otherslate
    print('Short returns are', endreturns, 'times your investment')
    print('Strategy returns are', endgains, 'times your investment')

#    s3[['LogRet', 'Strategy']].cumsum().apply(np.exp).plot(grid=True,
#                                                    figsize=(8, 5))
#    return s3[['LogRet', 'Strategy']].cumsum().apply(np.exp)
# a is long stop, b is short stop