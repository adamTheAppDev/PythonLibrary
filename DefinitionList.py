# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This program houses functions for use in scanners
#Performs a scan at the end, but can be used to import functions from.

#Get modules
import numpy as np
import pandas.io.data as web
import pandas as pd
from pandas import read_csv
from YahooGrabber import YahooGrabber

#Must use YahooGrabber for data request

#Read tickers into DataFrame 
df = read_csv('companylist.csv', sep = ',')
#Set index
df1 = df.set_index('Symbol')
#Assign column
symbols = df.Symbol.values
#Variable assignment
port = (symbols)
port1 = []
#Confirmation
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
