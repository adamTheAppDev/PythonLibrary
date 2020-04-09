# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is part of a kth fold optimization tool with a twist
#pandas_datareader is deprecated, use YahooGrabber

#Import modules
from DefModADXAdviceGiver import DefModADXAdviceGiver
import numpy as np
import pandas as pd
from pandas_datareader import data
#Read in param sets
Aggregate = pd.read_pickle('RUTModADXAGGSHARPE065')
Aggregate = Aggregate.loc[:,~Aggregate.columns.duplicated()]
#Assign ticker
ticker = '^RUT'
#Assign params
windowA = 15
windowB = 12
#Read in data
#s = data.DataReader(ticker, 'yahoo', start='04/01/2017', end='01/01/2050') 
s = pd.read_pickle('RUTModADXAGGAdvice07_50') # this is just for testing with a graph
#Add new data
#s2 = pd.DataFrame({'Open':[1411.05],'High':[1425.7],'Low':[1409.83],'Close':[0],'Volume':[0],
#'Adj Close':[1424.12]},index = ['2017-04-26 00:00:00']) #interday
#s = pd.concat([s,s2])
#Iterable
#ranger = range(1,len(s)+1)
#Incrementally longer time series
#dictionary = { r : s.loc[s.index[:r],:] for r in ranger}
#triumph = []
#for r in ranger:
#    q = dictionary[r]
#    result = DefModADXAdviceGiver(Aggregate, q)
#    triumph.append(result)  
#    print(r)
#    print(result)
#TheAdvice = pd.Series(triumph, index=s.index)
#s['Advice'] = TheAdvice

#Calculate log returns
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)
#Directional methodology
s['Regime'] = np.where(s['Advice'] > -1.874201, 1, 0)
s['Regime'] = np.where(s['Advice'] < -.328022, -1, s['Regime'])
#Apply position to returns 
s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
s['Strategy'] = s['Strategy'].fillna(0)
#Strategy w/ regime change
s['NewStrategy'] = s['Strategy']
#Intraday market width
s['Width'] = (s['High'] - s['Low'])/s['Open'] 
#Overnight volatility
s['OverNight'] = (s['Open'] - s['Adj Close'].shift(1))/s['Adj Close'].shift(1)
#Average volatility measure
s['RollingWidth'] = s['Width'].rolling(center = False, window=windowA).mean()
s['RollingOverNight'] = abs(s['OverNight']).rolling(center=False, window=windowB).mean()
#Difference in closing price
s['CloseDifference'] = (s['Adj Close'] / s['Adj Close'].shift(1))/s['Adj Close'].shift(1)
s['RollingCloseDifference'] = s['CloseDifference'].rolling(center = False, window=windowA).mean()
#Up days
s['DayUp'] = (s['High'] - s['Adj Close'].shift(1))/s['Open']
s['DayUp'] = s['DayUp'][s['DayUp']> 0]
s['DayUp'] = s['DayUp'].fillna(0)
#Down days
s['DayDown'] = (s['Adj Close'].shift(1) - s['Low'])/s['Open']
s['DayDown'] = s['DayDown'][s['DayDown']> 0]
s['DayDown'] = s['DayDown'].fillna(0)
#Performance metric
s['sharpe'] = (s['Strategy'].mean()-abs(s['LogRet'].mean()))/s['Strategy'].std()

#New regime methodology
s['LongGains'] = np.where(s['DayUp'] >= (s['RollingCloseDifference']),s['RollingCloseDifference'],0)
s['ShortGains'] = np.where(s['DayDown'] >= (s['RollingCloseDifference']),s['RollingCloseDifference'],0)
s['LongStop'] = np.where(s['OverNight'] <= (s['RollingCloseDifference'] * -1),
                                                s['OverNight'] ,0)
s['ShortStop'] = np.where(s['OverNight'] >= s['RollingCloseDifference'],
                                                (s['OverNight']*-1) ,0)
s['NewStrategy'] = np.where(s['Regime'].shift(1) == 1,s['LongGains'],0)
s['NewStrategy'] = np.where(s['Regime'].shift(1) == -1,s['ShortGains'],s['NewStrategy'])
s['NewStrategy'] = np.where(s['NewStrategy'] == 0, s['Strategy'], s['NewStrategy'])
s['NewStrategy'] = np.where(s['LongStop'] < 0, s['LongStop'], s['NewStrategy'])
s['NewStrategy'] = np.where(s['ShortStop'] < 0, s['ShortStop'], s['NewStrategy'])

#New performance metrics
s['newsharpe'] = (s['NewStrategy'].mean()-abs(s['LogRet'].mean()))/s['NewStrategy'].std() 
s['CorrectNextDay'] =  np.where(s['Regime'] == 1, s['High'].shift(
                                        -1) > s['Adj Close'] , 0)
s['CorrectNextDay'] =  np.where(s['Regime'] == -1, s['Low'].shift(
                         -1) < s['Adj Close'] , s['CorrectNextDay'])
winrate = sum(s['CorrectNextDay']/len(s)) #This is a bad metric

#Graphical display
#For increased accuracy, remove first window values from TheAdvice
s[['LogRet', 'NewStrategy','Strategy']][:].cumsum().apply(np.exp).plot(grid = True,
                                             figsize = (8,5))
#Display results
print(s)
print(s['sharpe'][-1])
print(s['newsharpe'][-1])
