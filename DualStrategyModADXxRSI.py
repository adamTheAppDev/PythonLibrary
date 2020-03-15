# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a two asset trading model

#Import modules
import numpy as np
import pandas as pd
fronm YahooGrabberII import YahooGrabberII
import pandas_datareader as pdr

#Assign variables
ticker = 'TMF'

#Read in pickles
ModADX = pd.read_pickle('TLTModADXAGGAdvice07_50')
RSI = pd.read_pickle('TLTAGGAdvice07_50')
ModADXOptimal = pd.read_pickle('TLTModADXAGGOptimal')
RSIOptimal = pd.read_pickle('TLTAGGOptimal')

#Data request, use YahooGrabberII
s = data.DataReader(ticker, 'yahoo', start='01/01/2007', end='03/21/2017') 

#Assign parameters
a = ModADXOptimal.iloc[0]
b = ModADXOptimal.iloc[1]
c = float(RSIOptimal.iloc[0])
d = float(RSIOptimal.iloc[1])

#Trim time series to match lengths
trim = len(ModADX) - len(RSI)
trim1 = len(ModADX) - trim
ModADX = ModADX[:trim1]

#Make dataframe to hold concatenated data
both = pd.DataFrame()
both['High'] = ModADX['High']
both['Low'] = ModADX['Low']
both['Open'] = ModADX['Open']
both['Adj Close'] = ModADX['Adj Close']
both['ModADXAdvice'] = ModADX['Advice']
both['RSIAdvice']  = RSI['Advice']

#Calculate log returns 
both['LogRet'] = np.log(both['Adj Close']/both['Adj Close'].shift(1)) 
both['LogRet'] = both['LogRet'].fillna(0)
#Separate model signals
both['ModADXRegime'] = np.where(both['ModADXAdvice'] > a, 1, 0)
both['ModADXRegime'] = np.where(both['ModADXAdvice'] < b, -1, both['ModADXRegime'])
both['RSIRegime'] = np.where(both['RSIAdvice'] > c, 1, 0)
both['RSIRegime'] = np.where(both['RSIAdvice'] < d, -1, both['RSIRegime'])
#Add signals 
both['SumRegimes'] = both['ModADXRegime'] + both['RSIRegime']
#Total direcitonal methodology
both['Regime'] = np.where(both['SumRegimes'] > 1, 1, 0)
both['Regime'] = np.where(both['SumRegimes'] < -1, -1, both['Regime'])
#Returns applied to direction
both['Strategy'] = (both['Regime']).shift(1)*both['LogRet']
both['Strategy'] = both['Strategy'].fillna(0)
#Strategy vs Return data // graphics
both[['LogRet', 'Strategy']].cumsum().apply(np.exp).plot(grid = True,
                                             figsize = (8,5))
#Performance metric
both['sharpe'] = (both['Strategy'].mean()-abs(both['LogRet'].mean(
                                                    )))/both['Strategy'].std()
#Display
print(both['sharpe'][-1])

#System statistic - CND
both['Correct'] =  np.where(both['Strategy'] > 0, 1, 0)
both['Correct'] =  np.where(both['Strategy'] < 0, -1, both['Correct'])
both['CorrectNextDay'] =  np.where(both['Regime'] == 1, both['High'].shift(
                                            -1) > both['Adj Close'] , 0)
both['CorrectNextDay'] =  np.where(both['Regime'] == -1, both['Low'].shift(
                             -1) < both['Adj Close'] , both['CorrectNextDay'])
both['ModCND'] = np.where(both['Regime'] == 0, 1, 0)
both['ModCND'] = both['ModCND'] + both['CorrectNextDay']
#Reassign regime
s['Regime'] = both['Regime']
#Calculate log returns
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)
#Calculate strategy returns
s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
s['Strategy'] = s['Strategy'].fillna(0)
#Returns vs strategy display
s[['LogRet', 'Strategy']].cumsum().apply(np.exp).plot(grid = True,
                                             figsize = (8,5))
#Performance metric
s['sharpe'] = (s['Strategy'].mean()-abs(s['LogRet'].mean(
                                                    )))/s['Strategy'].std()
#Display
print(s['sharpe'][-1])

#System statistic - CND
s['Correct'] =  np.where(s['Strategy'] > 0, 1, 0)
s['Correct'] =  np.where(s['Strategy'] < 0, -1, s['Correct'])

s['CorrectNextDay'] =  np.where(s['Regime'] == 1, s['High'].shift(
                                            -1) > s['Adj Close'] , 0)
s['CorrectNextDay'] =  np.where(s['Regime'] == -1, s['Low'].shift(
                             -1) < s['Adj Close'] , s['CorrectNextDay'])
s['ModCND'] = np.where(s['Regime'] == 0, 1, 0)
s['ModCND'] = s['ModCND'] + s['CorrectNextDay']
