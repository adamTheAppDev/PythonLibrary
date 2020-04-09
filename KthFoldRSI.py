# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is the first part of a kth fold optimization tool
#Its definitely written out the long way
#pandas_datareader is deprecated, use YahooGrabber

#Import modules
import numpy as np
from pandas_datareader import data
import random as rand
import pandas as pd
import time as t
from RelStrIndTester import RelStrIndTester
from RSIaggregate import RSIaggregate
#Empty structures
empty = [] 
#set up desired number of datasets for different period analysis
dataset1 = pd.DataFrame()
dataset2 = pd.DataFrame()
dataset3 = pd.DataFrame()
dataset4 = pd.DataFrame()
#Ticker assignment
ticker = 'DBC'
#This will correspond to dataset1
#Request data
s1 = data.DataReader(ticker, 'yahoo', start='01/01/2005', end='06/01/2009') 
#Calculate log returns
s1['LogRet'] = np.log(s1['Adj Close']/s1['Adj Close'].shift(1)) 
s1['LogRet'] = s1['LogRet'].fillna(0)
#This will correspond to dataset2
#Request data
s2 = data.DataReader(ticker, 'yahoo', start='06/01/2009', end='01/01/2013') 
#Calculate log returns
s2['LogRet'] = np.log(s2['Adj Close']/s2['Adj Close'].shift(1)) 
s2['LogRet'] = s2['LogRet'].fillna(0)
#This will correspond to dataset3
#Request data
s3 = data.DataReader(ticker, 'yahoo', start='01/01/2013', end='01/01/2050') 
#Calculate log returns
s3['LogRet'] = np.log(s3['Adj Close']/s3['Adj Close'].shift(1)) 
s3['LogRet'] = s3['LogRet'].fillna(0)
#This will correspond to dataset4
#Request data
s4 = data.DataReader(ticker, 'yahoo', start='01/01/2016', end='01/01/2050') 
#Calculate log returns
s4['LogRet'] = np.log(s4['Adj Close']/s4['Adj Close'].shift(1)) 
s4['LogRet'] = s4['LogRet'].fillna(0)
#Prep variables for RSI loops
close1 = s1['Adj Close']
close2 = s2['Adj Close']
close3 = s3['Adj Close']
close4 = s4['Adj Close']
#Number of iterations
iterations = range(0,1500000)
#Ignore error text display
np.seterr(divide='ignore', invalid='ignore')
#Get dataset 1 params
#Start timer
start1 = t.time()
#For number of iterations
for i in iterations:
    #Generate random params
    a = rand.randint(1,30)
    b = rand.random() * 100
    c = rand.random() * 100
    #Constraints
    if c < b:
        continue
    d = rand.random() * 100
    e = rand.random() * 100
    #Constraints
    if b > d:
        continue
    if c < e:
        continue
    #Variable assignment
    window = a  
    #RSI calculation
    delta1 = close1.diff()
    delta1 = delta1[1:]
    up1, down1 = delta1.copy(), delta1.copy()
    up1[up1 < 0] = 0
    down1[down1 > 0] = 0
    AvgGain1 = up1.rolling(window).mean()
    AvgGain1 = AvgGain1.fillna(0)
    AvgLoss1 = down1.abs().rolling(window).mean()
    AvgLoss1 = AvgLoss1.fillna(0)
    RS1 = AvgGain1/AvgLoss1
    RS1 = RS1.fillna(0)
    RSI1 = 100 - (100/(1.0+RS1))
    s1['RSI'] = RSI1
    s1['RSI'] = s1['RSI'].fillna(0)
    #Directional methodology
    s1['Touch'] = np.where(s1['RSI'] < b, 1, 0) #long signal
    s1['Touch'] = np.where(s1['RSI'] > c, -1, s1['Touch']) #short signal
    s1['Sustain'] = np.where(s1['Touch'].shift(1) == 1, 1, 0) 
    s1['Sustain'] = np.where(s1['Sustain'].shift(1) == 1, 1, 
                                         s1['Sustain']) 
    s1['Sustain'] = np.where(s1['Touch'].shift(1) == -1, -1, 0) 
    s1['Sustain'] = np.where(s1['Sustain'].shift(1) == -1, -1, 
                                     s1['Sustain']) #short
    s1['Sustain'] = np.where(s1['RSI'] > d, 0, s1['Sustain']) 
    s1['Sustain'] = np.where(s1['RSI'] < e, 0, s1['Sustain']) 
    s1['Regime'] = s1['Touch'] + s1['Sustain']
    #Apply position to returns
    s1['Strategy'] = (s1['Regime']).shift(1)*s1['LogRet']
    s1['Strategy'] = s1['Strategy'].fillna(0)
    #Ones
    endgains1 = 1
    endreturns1 = 1
    #Compounding returns
    for g in s1['LogRet']:
        slate1 = endreturns1 * (1+g)
        endreturns1 = slate1
    for q in s1['Strategy']:
        otherslate1 = endgains1 * (1+q)
        endgains1 = otherslate1
    #Constraints
    if endreturns1 > endgains1:
        continue
    if s1['Strategy'].std() == 0:
        continue
    #Performance metrics
    sharpe1 = (s1['Strategy'].mean()-abs(s1['LogRet'].mean()))/s1['Strategy'].std()
    #Constraints
    if sharpe1 < 0.03:
        continue
    #Save params and metrics to list
    empty.append(a)
    empty.append(b)
    empty.append(c)
    empty.append(d)
    empty.append(e)
    empty.append(endreturns1)
    empty.append(endgains1)
    empty.append(sharpe1)
    #List to Series
    emptyseries1 = pd.Series(empty)
    #Series to dataframe
    dataset1[i] = emptyseries1.values
    #Clear list
    empty[:] = []   
#End timer
end1 = t.time()
#Metric of choice
z1 = dataset1.iloc[7]
#Threshold
w1 = np.percentile(z1, 80)
v1 = [] #this variable stores the Nth percentile of top params
DS1W = pd.DataFrame() #this variable stores your params for specific dataset
#For all metrics
for h in z1:
    #If greater than threshold
    if h > w1:
      #Add to list
      v1.append(h)
#For top metrics
for j in v1:
      #Get column ID of metric
      r = dataset1.columns[(dataset1 == j).iloc[7]]    
      #Add param set to dataframe
      DS1W = pd.concat([DS1W,dataset1[r]], axis = 1)
#Top param
#y = max(z1)
#Column ID of top paramset
#x = dataset1.columns[(dataset1 == y).iloc[7]] 
#Top param set
#print(dataset1[x])
#Timer stats
print('Dataset 1 is optimized, it took',end1-start1,'seconds')

#Find params from dataset2
start2 = t.time()
#For number of iterations
for i in iterations:
    #Generate random params
    a = rand.randint(1,30)
    b = rand.random() * 100
    c = rand.random() * 100
    #Constraints
    if c < b:
        continue
    d = rand.random() * 100
    e = rand.random() * 100
    #Constraints
    if b > d:
        continue
    if c < e:
        continue
    #Variable assignment
    window = a  
    #RSI calculation
    delta2 = close2.diff()
    delta2 = delta2[1:]
    up2, down2 = delta2.copy(), delta2.copy()
    up2[up2 < 0] = 0
    down2[down2 > 0] = 0
    AvgGain2 = up2.rolling(window).mean()
    AvgGain2 = AvgGain2.fillna(0)
    AvgLoss2 = down2.abs().rolling(window).mean()
    AvgLoss2 = AvgLoss2.fillna(0)
    RS2 = AvgGain2/AvgLoss2
    RS2 = RS2.fillna(0)
    RSI2 = 100 - (100/(1.0+RS2))
    s2['RSI'] = RSI2
    s2['RSI'] = s2['RSI'].fillna(0)
    #Directional methodology
    s2['Touch'] = np.where(s2['RSI'] < b, 1, 0) #long signal
    s2['Touch'] = np.where(s2['RSI'] > c, -1, s2['Touch']) #short signal
    s2['Sustain'] = np.where(s2['Touch'].shift(1) == 1, 1, 0) 
    s2['Sustain'] = np.where(s2['Sustain'].shift(1) == 1, 1, 
                                         s2['Sustain'])
    s2['Sustain'] = np.where(s2['Touch'].shift(1) == -1, -1, 0) 
    s2['Sustain'] = np.where(s2['Sustain'].shift(1) == -1, -1, 
                                     s2['Sustain']) 
    s2['Sustain'] = np.where(s2['RSI'] > d, 0, s2['Sustain']) 
    s2['Sustain'] = np.where(s2['RSI'] < e, 0, s2['Sustain']) 
    s2['Regime'] = s2['Touch'] + s2['Sustain']
    #Apply position to returns
    s2['Strategy'] = (s2['Regime']).shift(1)*s2['LogRet']
    s2['Strategy'] = s2['Strategy'].fillna(0)
    #Ones
    endgains2 = 1
    endreturns2 = 1
    #Compounding returns
    for g in s2['LogRet']:
        slate2 = endreturns2 * (1+g)
        endreturns2 = slate2
    for q in s2['Strategy']:
        otherslate2 = endgains2 * (1+q)
        endgains2 = otherslate2
    #Constraints
    if endreturns2 > endgains2:
        continue
    if s2['Strategy'].std() == 0:
        continue
    #Performance metrics
    sharpe2 = (s2['Strategy'].mean()-abs(s2['LogRet'].mean()))/s2['Strategy'].std()
    #Constraints
    if sharpe2 < 0.026:
        continue
    #Save params and metrics to list
    empty.append(a)
    empty.append(b)
    empty.append(c)
    empty.append(d)
    empty.append(e)
    empty.append(endreturns2)
    empty.append(endgains2)
    empty.append(sharpe2)
    #List to Series
    emptyseries2 = pd.Series(empty)
    #Series to dataframe
    dataset2[i] = emptyseries2.values
    #Clear list
    empty[:] = []
#End timer
end2 = t.time()
#Metric of choice
z2 = dataset2.iloc[7]
#Threshold
w2 = np.percentile(z2, 80)
v2 = [] #this variable stores the Nth percentile of top params
DS2W = pd.DataFrame() #this variable stores your params for specific dataset
#For all metrics
for h in z2:
    #If greater than threshold
    if h > w2:
      #Add to list
      v2.append(h)
#For top metrics
for j in v2:
      #Get column ID of metric
      r = dataset2.columns[(dataset2 == j).iloc[7]] 
      #Add param set to dataframe
      DS2W = pd.concat([DS2W,dataset2[r]], axis = 1)
#Top metric
#y = max(z)
#Column ID of top paramset
#x = dataset2.columns[(dataset2 == y).iloc[7]] 
#Top param set
#print(dataset2[x])
#Timer stats
print('Dataset 2 is optimized, it took',end2-start2,'seconds') 

#Find params from dataset3
start3 = t.time()
#For number of iterations
for i in iterations:
    #Generate random params
    a = rand.randint(1,30)
    b = rand.random() * 100
    c = rand.random() * 100
    #Constraints
    if c < b:
        continue
    d = rand.random() * 100
    e = rand.random() * 100
    #Constraints
    if b > d:
        continue
    if c < e:
        continue
    #Variable assignment
    window = a  
    #RSI calculation
    delta3 = close3.diff()
    delta3 = delta3[1:]
    up3, down3 = delta3.copy(), delta3.copy()
    up3[up3 < 0] = 0
    down3[down3 > 0] = 0
    AvgGain3 = up3.rolling(window).mean()
    AvgGain3 = AvgGain3.fillna(0)
    AvgLoss3 = down3.abs().rolling(window).mean()
    AvgLoss3 = AvgLoss3.fillna(0)
    RS3 = AvgGain3/AvgLoss3
    RS3 = RS3.fillna(0)
    RSI3 = 100 - (100/(1.0+RS3))
    s3['RSI'] = RSI3
    s3['RSI'] = s3['RSI'].fillna(0)
    #Directional methodology
    s3['Touch'] = np.where(s3['RSI'] < b, 1, 0) #long signal
    s3['Touch'] = np.where(s3['RSI'] > c, -1, s3['Touch']) #short signal
    s3['Sustain'] = np.where(s3['Touch'].shift(1) == 1, 1, 0) 
    s3['Sustain'] = np.where(s3['Sustain'].shift(1) == 1, 1, 
                                         s3['Sustain']) 
    s3['Sustain'] = np.where(s3['Touch'].shift(1) == -1, -1, 0)  
    s3['Sustain'] = np.where(s3['Sustain'].shift(1) == -1, -1, 
                                     s3['Sustain']) 
    s3['Sustain'] = np.where(s3['RSI'] > d, 0, s3['Sustain']) 
    s3['Sustain'] = np.where(s3['RSI'] < e, 0, s3['Sustain']) 
    s3['Regime'] = s3['Touch'] + s3['Sustain']
    #Apply position to returns
    s3['Strategy'] = (s3['Regime']).shift(1)*s3['LogRet']
    s3['Strategy'] = s3['Strategy'].fillna(0)
    #Ones
    endgains3 = 1
    endreturns3 = 1
    #Compounding returns
    for g in s3['LogRet']:
        slate3 = endreturns3 * (1+g)
        endreturns3 = slate3
    for q in s3['Strategy']:
        otherslate3 = endgains3 * (1+q)
        endgains3 = otherslate3
    #Constraints
    if endreturns3 > endgains3:
        continue
    if s3['Strategy'].std() == 0:
        continue    
    #Performance metrics
    sharpe3 = (s3['Strategy'].mean()-abs(s3['LogRet'].mean()))/s3['Strategy'].std()
    #Constraints
    if sharpe3 < 0.038:
        continue
    #Save params and metrics to list
    empty.append(a)
    empty.append(b)
    empty.append(c)
    empty.append(d)
    empty.append(e)
    empty.append(endreturns3)
    empty.append(endgains3)
    empty.append(sharpe3)
    #List to Series
    emptyseries3 = pd.Series(empty)
    #Series to dataframe
    dataset3[i] = emptyseries3.values
    #Clear list
    empty[:] = []
#End timer
end3 = t.time()
#Metric of choice
z3 = dataset3.iloc[7]
#Threshold
w3 = np.percentile(z3, 80)
v3 = [] #this variable stores the Nth percentile of top params
DS3W = pd.DataFrame() #this variable stores your params for specific dataset
#For all metrics
for h in z3:
    #If greater than threshold
    if h > w3:
      #Add to list
      v3.append(h)
#For top metrics
for j in v3:
      #Get column ID of metric
      r = dataset3.columns[(dataset3 == j).iloc[7]] 
      #Add param set to dataframe
      DS3W = pd.concat([DS3W,dataset3[r]], axis = 1)
#Top metric
#y = max(z)
#Column ID of top paramset
#x = dataset3.columns[(dataset3 == y).iloc[7]] 
#Top param set
#print(dataset3[x])
#Timer stats
print('Dataset 3 is optimized, it took',end3-start3,'seconds') 

#Find params from dataset4
start4 = t.time()
#For number of iterations
for i in iterations:
    #Generate random params
    a = rand.randint(1,30)
    b = rand.random() * 100
    c = rand.random() * 100
    #Constraints
    if c < b:
        continue
    d = rand.random() * 100
    e = rand.random() * 100
    #Constraints
    if b > d:
        continue
    if c < e:
        continue
    #Variable assignment
    window = a  
    #RSI calculation
    delta4 = close4.diff()
    delta4 = delta4[1:]
    up4, down4 = delta4.copy(), delta4.copy()
    up4[up4 < 0] = 0
    down4[down4 > 0] = 0
    AvgGain4 = up4.rolling(window).mean()
    AvgGain4 = AvgGain4.fillna(0)
    AvgLoss4 = down4.abs().rolling(window).mean()
    AvgLoss4 = AvgLoss4.fillna(0)
    RS4 = AvgGain4/AvgLoss4
    RS4 = RS4.fillna(0)
    RSI4 = 100 - (100/(1.0+RS4))
    s4['RSI'] = RSI4
    s4['RSI'] = s4['RSI'].fillna(0)
    #Directional methodology
    s4['Touch'] = np.where(s4['RSI'] < b, 1, 0) #long signal
    s4['Touch'] = np.where(s4['RSI'] > c, -1, s4['Touch']) #short signal
    s4['Sustain'] = np.where(s4['Touch'].shift(1) == 1, 1, 0) 
    s4['Sustain'] = np.where(s4['Sustain'].shift(1) == 1, 1, 
                                         s4['Sustain']) 
    s4['Sustain'] = np.where(s4['Touch'].shift(1) == -1, -1, 0) 
    s4['Sustain'] = np.where(s4['Sustain'].shift(1) == -1, -1, 
                                     s4['Sustain'])
    s4['Sustain'] = np.where(s4['RSI'] > d, 0, s4['Sustain']) 
    s4['Sustain'] = np.where(s4['RSI'] < e, 0, s4['Sustain']) 
    s4['Regime'] = s4['Touch'] + s4['Sustain']
    #Apply position to returns
    s4['Strategy'] = (s4['Regime']).shift(1)*s4['LogRet']
    s4['Strategy'] = s4['Strategy'].fillna(0)
    #Ones
    endgains4 = 1
    endreturns4 = 1
    #Compounding returns
    for g in s4['LogRet']:
        slate4 = endreturns4 * (1+g)
        endreturns4 = slate4
    for q in s4['Strategy']:
        otherslate4 = endgains4 * (1+q)
        endgains4 = otherslate4
    #Constraints
    if endreturns4 > endgains4:
        continue
    if s4['Strategy'].std() == 0:
        continue    
    #Performance metrics
    sharpe4 = (s4['Strategy'].mean()-abs(s4['LogRet'].mean()))/s4['Strategy'].std()
    #Constraints
    if sharpe4 < 0.04:
        continue
    #Save params and metrics to list
    empty.append(a)
    empty.append(b)
    empty.append(c)
    empty.append(d)
    empty.append(e)
    empty.append(endreturns4)
    empty.append(endgains4)
    empty.append(sharpe4)
    #List to Series
    emptyseries4 = pd.Series(empty)
    #Series to dataframe
    dataset4[i] = emptyseries4.values
    #Clear list
    empty[:] = []   
#End timer
end4 = t.time()
#Metric of choice
z4 = dataset4.iloc[7]
#Threshold
w4 = np.percentile(z4, 80)
v4 = [] #this variable stores the Nth percentile of top params
DS4W = pd.DataFrame() #this variable stores your params for specific dataset
#For all metrics
for h in z4:
    #If greater than threshold
    if h > w4:
      #Add to list
      v4.append(h)
#For top metrics
for j in v4:
      #Get column ID of metric
      r = dataset4.columns[(dataset4 == j).iloc[7]]    
      #Add param set to dataframe
      DS4W = pd.concat([DS4W,dataset4[r]], axis = 1)
#Top metric
#y = max(z)
#Column ID of top paramset
#x = dataset4.columns[(dataset4 == y).iloc[7]] 
#Top param set
#print(dataset4[x]) 
#Timer stats
print('Dataset 4 is optimized, it took',end4-start4,'seconds')

#Create the test sets
S1TS = pd.DataFrame()
S2TS = pd.DataFrame()
S3TS = pd.DataFrame()
S4TS = pd.DataFrame()

#remove duplicate columns
DS1W = DS1W.loc[:,~DS1W.columns.duplicated()]
DS2W = DS2W.loc[:,~DS2W.columns.duplicated()]
DS3W = DS3W.loc[:,~DS3W.columns.duplicated()]
DS4W = DS4W.loc[:,~DS4W.columns.duplicated()]

#merge winners to create test sets
S1TS = pd.concat([S1TS, DS2W, DS3W, DS4W], axis = 1)
S2TS = pd.concat([S2TS, DS1W, DS3W, DS4W], axis = 1)
S3TS = pd.concat([S3TS, DS1W, DS2W, DS4W], axis = 1)
S4TS = pd.concat([S4TS, DS1W, DS2W, DS3W], axis = 1)

#Test the test sets
Aggregate = RelStrIndTester(s1,s2,s3,s4,S1TS,S2TS,S3TS,S4TS)

#Remove duplicates columns
Aggregate = Aggregate.loc[:,~Aggregate.columns.duplicated()]

#Test aggregate params in latest time series
advice = RSIaggregate(s4, Aggregate)
print(advice)
