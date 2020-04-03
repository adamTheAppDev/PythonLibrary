# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a kth fold optimization tool with a brute force optimizer + a twist
#pandas_datareader is deprecated, use YahooGrabber

#Import modules
import numpy as np
import pandas as pd
import random as rand
#from pandas_datareader import data

#Read in data
Aggregate = pd.read_pickle('RUTModADXAGGSHARPE065')
#Remove duplicate columns
Aggregate = Aggregate.loc[:,~Aggregate.columns.duplicated()]
#Assign ticker
ticker = '^RUT'
#Request/read in data
#s = data.DataReader(ticker, 'yahoo', start='04/01/2017', end='01/01/2050') 
s = pd.read_pickle('RUTModADXAGGAdvice07_50') # this is just for testing with a graph
#Number of iterations for optimization
iterations = 5000
#Iterable range
ranger = range(0,iterations)
#Empty data structures
empty = []
counter = 0
dataset = pd.DataFrame()

#For number of iterations
for r in ranger: 
    #Iteration tracking
    print(counter)
    counter = counter+1
    
    #Generate random params
    a = rand.randint(2,15)
    b = rand.randint(2,15)
    c = rand.random() * 3
    d = rand.random() * 3
    e = rand.random() * 3
    f = rand.random() * 3
    
    #Calculate log returns
    s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
    s['LogRet'] = s['LogRet'].fillna(0)
    #Directional methodology
    s['Regime'] = np.where(s['Advice'] > -1.874201, 1, 0)
    s['Regime'] = np.where(s['Advice'] < -.328022, -1, s['Regime'])
    #Direction applied to returns
    s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
    s['Strategy'] = s['Strategy'].fillna(0)
    #Copy
    s['NewStrategy'] = s['Strategy']
    #Market width
    s['Width'] = (s['High'] - s['Low'])/s['Open'] 
    #Overnight move
    s['OverNight'] = (s['Open'] - s['Adj Close'].shift(1))/s['Adj Close'].shift(1)
    #Averages
    s['RollingWidth'] = s['Width'].rolling(center = False, window=a).mean()
    s['RollingOverNight'] = abs(s['OverNight']).rolling(center=False, window=b).mean()
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
    #Profit takers
    s['LongGains'] = np.where(s['DayUp'] >= (s['RollingWidth']/c),s['RollingWidth']/c,0)
    s['ShortGains'] = np.where(s['DayDown'] >= (s['RollingWidth']/d),s['RollingWidth']/d,0)
    #Stop losses
    s['LongStop'] = np.where(s['OverNight'] <= (s['RollingWidth'].shift(1)/e * -1),
                                                    s['OverNight'] ,0)
    s['ShortStop'] = np.where(s['OverNight'] >= s['RollingWidth'].shift(1)/f,
                                                    (s['OverNight']*-1) ,0)
    #Implement profit take/stop loss
    s['NewStrategy'] = np.where(s['Regime'].shift(1) == 1,s['LongGains'],0)
    s['NewStrategy'] = np.where(s['Regime'].shift(1) == -1,s['ShortGains'],s['NewStrategy'])
    s['NewStrategy'] = np.where(s['NewStrategy'] == 0, s['Strategy'], s['NewStrategy'])
    s['NewStrategy'] = np.where(s['LongStop'] < 0, s['LongStop'], s['NewStrategy'])
    s['NewStrategy'] = np.where(s['ShortStop'] < 0, s['ShortStop'], s['NewStrategy'])
    #New strategy metric
    s['newsharpe'] = (s['NewStrategy'].mean()-abs(s['LogRet'].mean()))/s['NewStrategy'].std()  
    #Constraint
    if s['newsharpe'][-1] < .04:
        continue
    #Save params and metrics to list
    empty.append(a)
    empty.append(b)
    empty.append(c)
    empty.append(d)
    empty.append(e)
    empty.append(f)
    empty.append(s['sharpe'][-1])
    empty.append(s['newsharpe'][-1])    
    #List to Series
    emptyseries = pd.Series(empty)
    #Series to dataframe
    dataset[r] = emptyseries.values
    #Clear list
    empty[:] = []     
#Metric to sort
z = dataset.iloc[7]
#Threshold
w = np.percentile(z, 80)
v = [] #this variable stores the Nth percentile of top params
DS1W = pd.DataFrame() #this variable stores your params for specific dataset
#Sort with threshold
for h in z:
    if h > w:
      v.append(h)
#Add to dataframe
for j in v:
      r = dataset.columns[(dataset == j).iloc[7]]    
      DS1W = pd.concat([DS1W,dataset[r]], axis = 1)
#Top metric
y = max(z)
#Top metric column number
x = dataset.columns[(dataset == y).iloc[7]] 
#Top param set
print(dataset[x])
#Display metrics
#print(s)
#print(s['sharpe'][-1])
#print(s['newsharpe'][-1])
