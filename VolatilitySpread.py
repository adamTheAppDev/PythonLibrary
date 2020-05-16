# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a strategy tester for volatility

#Import modules
import numpy as np
from pandas_datareader import data

#Request data
s = data.DataReader('^VIX', 'yahoo', start='1/1/1900', end='01/01/2050') 
s2 = data.DataReader('^VXV', 'yahoo', start='1/1/1900', end='01/01/2050') 
s3 = data.DataReader('VXX', 'yahoo', start='1/1/1900', end='01/01/2050')

#Define function
def ShortVol(x, y):
    #Calculate log returns
    s3['LogRet'] = np.log(s3['Adj Close']/s3['Adj Close'].shift(1))
    s3['LogRet'] = s3['LogRet'].fillna(0)
    #Price relative
    s3['Meter'] = s['Close']/s2['Close']
    s3['Meter'].plot(grid=True, figsize=(8, 5))
    #Directional methodology
    s3['Touch'] = np.where(s3['Meter'] < x, -1, 0) # short signal
    s3['Touch'] = np.where(s3['Meter'] > y, 0, s3['Touch']) #flat signal
    s3['Sustain'] = np.where(s3['Touch'].shift(1) == -1, -1, 0) #short
    s3['Sustain'] = np.where(s3['Sustain'].shift(1) == -1, -1, #stays
                                         s3['Sustain']) #short
    s3['Sustain'] = np.where(s3['Touch'].shift(1) == 0, 0, 0) #flat
    s3['Sustain'] = np.where(s3['Sustain'].shift(1) == 0, 0, #stays
                                         s3['Sustain']) #flat
    #Directional methodology
    s3['Regime'] = s3['Touch'] + s3['Sustain']
    #Apply position to returns
    s3['Strategy'] = (s3['Regime']).shift(1)*s3['LogRet']
    s3['Strategy'] = s3['Strategy'].fillna(0)
    
    #Ones
    endgains = 1
    endreturns = 1
    #Empty lists
    returnstream = []
    gainstream = []
    #Apply returns
    for i in s3['LogRet']:
        slate = endreturns * (1+-i)
        returnstream.append(slate)
        endreturns = slate
    for i in s3['Strategy']:
        otherslate = endgains * (1+i)
        gainstream.append(otherslate)
        endgains = otherslate
    #Display results    
    print('Short returns are', endreturns, 'times your investment')
    print('Strategy returns are', endgains, 'times your investment')
