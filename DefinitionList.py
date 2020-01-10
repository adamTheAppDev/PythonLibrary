# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 21:45:57 2016

@author: AmatVictoriaCuramIII
"""

#When executed, this program is just a database scanner. 
#Nothing real special. Didn't actually finish whatever it was I set to do here..

#Get modules
import numpy as np
import pandas.io.data as web
import pandas as pd
from pandas import read_csv
#Import and define info the list 
df = read_csv('companylist.csv', sep = ',')
df1 = df.set_index('Symbol')
symbols = df.Symbol.values
port = (symbols)
port1 = []
print(symbols)
#Build search parameters
def Age(s):
    s = web.get_data_yahoo(s, start='1/1/1900', end='01/01/2018')
    return len(s['Adj Close'])
def Mean(s):
    s = web.get_data_yahoo(s, start='1/1/1900', end='01/01/2018')
    s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1))
    s['Mean'] = np.mean(s['LogRet'])*252
    return s['Mean'].tail(1)
def SD(s):
    s = web.get_data_yahoo(s, start='1/1/1900', end='01/01/2018')
    s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1))
    s['SD'] = np.std(s['LogRet'])*np.sqrt(252)
    return s['SD'].tail(1)
def SDSD(s):
    s = web.get_data_yahoo(s, start='1/1/1900', end='01/01/2018')
    s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1))
    s['SD'] = np.sqrt(pd.rolling_var(s['LogRet']*np.sqrt(252), window=252))
    s['SDSD'] = np.std(s['SD']*np.sqrt(252))
    return s['SDSD'].tail(1)
def Trend(s):# + denotes bullish, - denotes bearish
    s = web.get_data_yahoo(s, start='1/1/1900', end='01/01/2018')
    s['42d'] = np.round(pd.rolling_mean(s['Adj Close'], window=42), 2)
    s['252d'] = np.round(pd.rolling_mean(s['Adj Close'], window = 252), 2)
#graphs    s[['Close', '42d', '252d']].plot(grid=True, figsize=(8, 5))
    s['42-252'] = s['42d'] - s['252d']
    s['Trend'] = (s['42-252']/s['Adj Close']).dropna()
    return s['Trend'].tail(1)
def CoeffVar(s):
    s = web.get_data_yahoo(s, start='1/1/1900', end='01/01/2018')
    s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1))
    s['Mean'] = np.mean(s['LogRet'])*252
    s['SD'] = np.std(s['LogRet'])*np.sqrt(252)
    s['CoeffVar'] = s['Mean']/s['SD']
    return s['CoeffVar'].tail(1)
def AvgVolume(s):
    s = web.get_data_yahoo(s, start='1/1/1900', end='01/01/2018')
    s['AverageVolume'] = (sum(s['Volume']) / len(s['Volume']))
    return s['AverageVolume'].tail(1)
def MovingAverages(s):
    s = web.get_data_yahoo(s, start='1/1/1900', end='01/01/2018')
    s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1))
    s['42d'] = np.round(pd.rolling_mean(s['Adj Close'], window=42), 2)
    s['252d'] = np.round(pd.rolling_mean(s['Adj Close'],
                                             window = 252), 2)
    s['42-252'] = s['42d'] - s['252d']
    s['Trend']= s['42-252']/s['Adj Close']
    s['Touch'] = np.where(s['42-252'] > .03, 1, 0)
    s['Touch'] = np.where(s['42-252'] < -.03, -1, s['Touch'])
    s['Sustain'] = np.where(s['Touch'].shift(1) == 1, 1, 0)
    s['Sustain'] = np.where(s['Sustain'].shift(1) == 1, 1,
                                         s['Sustain'])
    s['Sustain'] = np.where(s['Touch'].shift(1) == -1, -1, 0)
    s['Sustain'] = np.where(s['Sustain'].shift(1) == -1, -1,
                                         s['Sustain'])
    s['Sustain'] = np.where(s['42-252'] > .10, 0, s['Sustain'])
    s['Sustain'] = np.where(s['42-252'] < -.10 , 0, s['Sustain'])
    s['Regime'] = s['Touch'] + s['Sustain']
    s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
    s[['LogRet', 'Strategy']].cumsum().apply(np.exp).plot(grid=True,
                                                    figsize=(8, 5))
    s[['42d', '252d', 'Close']].plot(grid=True, figsize=(8, 5))
    return s['Strategy']       
def RelStrInd(s):
    s = web.get_data_yahoo(s, start='1/1/1900', end='01/01/2018')
    close = s['Adj Close']
    window = 14    
    delta = close.diff()
    delta = delta[1:]
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    AvgGain = up.rolling(window).mean()
    AvgLoss = down.abs().rolling(window).mean() 
    RS = AvgGain/AvgLoss
    RSI = 100 - (100/(1.0+RS))
#    RSI.plot(grid=True, figsize=(8, 5))
    return RSI.tail(1)
def Execution(s):
    s = web.get_data_yahoo(s, start='1/1/1900', end='01/01/2018')
    s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
    close = s['Adj Close']
    window = 14   
    delta = close.diff()
    delta = delta[1:]
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    AvgGain = up.rolling(window).mean()
    AvgLoss = down.abs().rolling(window).mean() 
    RS = AvgGain/AvgLoss
    RSI = 100 - (100/(1.0+RS))
    s['RSI'] = RSI
    s['Touch'] = np.where(s['RSI'] < .55, 1, 0)
    s['Touch'] = np.where(s['RSI'] > .45, -1, s['Touch'])
    s['Sustain'] = np.where(s['Touch'].shift(1) == 1, 1, 0)
    s['Sustain'] = np.where(s['Sustain'].shift(1) == 1, 1,
                                         s['Sustain'])
    s['Sustain'] = np.where(s['Touch'].shift(1) == -1, -1, 0)
    s['Sustain'] = np.where(s['Sustain'].shift(1) == -1, -1,
                                         s['Sustain'])
    s['Sustain'] = np.where(s['RSI'] > .55, 0, s['Sustain'])
    s['Sustain'] = np.where(s['RSI'] < .45, 0, s['Sustain'])
    s['Regime'] = s['Touch'] + s['Sustain']
    s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
    s[['LogRet', 'Strategy']].cumsum().apply(np.exp).plot(grid=True,
                                                    figsize=(8, 5))
    print(s['Strategy'].std())
    print(s['Strategy'].mean())
#    c = s['Strategy'].mean()
#    d = s['Strategy'].std()
#    return s['Strategy']
#    f[0] = -1*((c^2)/d)  
#    return f[0]
def ShortVol(x, y):
    s = web.get_data_yahoo('^VIX', start='1/1/1900', end='01/01/2018') 
    s2 = web.get_data_yahoo('^VXV', start='1/1/1900', end='01/01/2018') 
    s3 = web.get_data_yahoo('VXX', start='1/1/1900', end='01/01/2018')
    s3['LogRet'] = np.log(s3['Adj Close']/s3['Adj Close'].shift(1))
    s3['Meter'] = s['Close']/s2['Close']
    print(s3['Meter'])
    s3['Meter'].plot(grid=True, figsize=(8, 5))
    s3['Touch'] = np.where(s3['Meter'] > x, -1, 0)
    s3['Touch'] = np.where(s3['Meter'] < y, 0, s3['Touch'])
    s3['Sustain'] = np.where(s3['Touch'].shift(1) == -1, -1, 0)
    s3['Sustain'] = np.where(s3['Sustain'].shift(1) == -1, -1,
                                         s3['Sustain'])
    s3['Sustain'] = np.where(s3['Touch'].shift(1) == 0, 0, 0)
    s3['Sustain'] = np.where(s3['Sustain'].shift(1) == 0, 0,
                                         s3['Sustain'])
#    s3['Sustain'] = np.where(s3['Meter'] < .8, 0, s3['Sustain'])
    s3['Regime'] = s3['Touch'] + s3['Sustain']
    s3['Strategy'] = (s3['Regime']).shift(1)*s3['LogRet']
    s3[['LogRet', 'Strategy']].cumsum().apply(np.exp).plot(grid=True,
                                                    figsize=(8, 5))
    return s3[['LogRet', 'Strategy']].cumsum().apply(np.exp)
# y is long signal, z is short signal, a is long stop, b is short stop
#Scan and filter
for s in port:
    try:
        if Age(s) > 1000 and sum(Mean(s)) < -.1 and sum(CoeffVar(s)) < -.5 and sum(
               Trend(s)) < -0.04 and sum(RelStrInd(s)) > 60:
            print(s, Mean(s), Trend(s), CoeffVar(s), Age(s), RelStrInd(s))
            port1.append(s)
    except OSError:
        pass
#List refined portfolio
print(port1)
df2 = pd.DataFrame([])
#Set up new parameters
cash = 100000
#Implement logic
def WxR(port):
    numsec = len(port)
    ws = 1/numsec
    df2 = pd.DataFrame(columns=[])
    for s in port:
        s = web.get_data_yahoo(s, start='1/1/1990', end='01/01/2018') 
        s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1))
        s['ws'] = ws
        df2 = pd.concat([df2,s['LogRet']], axis=1)
#    df2 = df2.assign(s=s['LogRet'].values)
    print(df2)
