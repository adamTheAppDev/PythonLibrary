# -*- coding: utf-8 -*-
"""
Created on Sun Jun 11 19:26:12 2017

@author: AmatVictoriaCuramIII
"""

#This is mostly a technical analysis tool
#provides the basic structure/idea for Database Modification

import numpy as np
import pandas as pd

temp = pd.read_pickle('/Users/AmatVictoriaCuramIII/Desktop/PythonFiles/QQQAGGAdvice07_50')
ranger = range(0,len(temp['Adj Close']))
index = temp.index
#transfer to database modification

temp['LogRet'] = np.log(temp['Adj Close']/temp['Adj Close'].shift(1)) 
temp['LogRet'] = temp['LogRet'].fillna(0)

temp['52wkLow'] = temp['Adj Close'].rolling(252).min()
temp['52wkMax'] = temp['Adj Close'].rolling(252).max()

temp['Age'] = len(temp['Open'])

temp['TotalAverageAnnualReturn'] = temp['LogRet'].mean() * 252

temp['TotalAverageAnnualStandardDeviation'] = temp['LogRet'].std(
                                                     )*np.sqrt(252)

temp['CoefficientOfVaration'] = (
temp['TotalAverageAnnualStandardDeviation']/temp['TotalAverageAnnualReturn'])

temp['Rolling52wkMockReturn'] = temp['LogRet'].rolling(
                                 center=False, window = 252).mean()

temp['Rolling52wkReturn'] = np.log(temp['Adj Close']/
                                     temp['Adj Close'].shift(252))

temp['Rolling52wkStandardDeviation'] = temp['LogRet'].rolling(
                                center = False, window = 252).std()

temp['Rolling4wkStandardDeviation'] = temp['LogRet'].rolling(
                                 center = False, window = 20).std()

temp['AverageAnnualRollingVolume'] = temp['Volume'].rolling(
                                   center=False, window=252).mean()

temp['Rolling52wkCoefficientOfVariation'] = (
    temp['Rolling52wkStandardDeviation']/temp['Rolling52wkReturn'])

temp['Rolling52wkDoubleStandardDeviation'] = (
    temp['Rolling52wkStandardDeviation'].rolling(
    center = False, window = 252))

temp['4wkOver52wkStandardDeviationRatio'] = (
    temp['Rolling4wkStandardDeviation']/temp['Rolling52wkStandardDeviation'])    

# ADX with PDI, MDI, ADX, ADXmean, TrueRange, AverageTrueRange, ADXStrength
ADXwindow = 14
temp['ADXUpMove'] = temp['High'] - temp['High'].shift(1)
temp['ADXDownMove'] = temp['Low'] - temp['Low'].shift(1)
temp['Method1'] = temp['High'] - temp['Low']
temp['Method2'] = abs((temp['High'] - temp['Adj Close'].shift(1)))
temp['Method3'] = abs((temp['Low'] - temp['Adj Close'].shift(1)))
temp['Method1'] = temp['Method1'].fillna(0)
temp['Method2'] = temp['Method2'].fillna(0)
temp['Method3'] = temp['Method3'].fillna(0)
temp['TrueRange'] = temp[['Method1','Method2','Method3']].max(axis = 1)
temp['AverageTrueRange'] = temp['TrueRange'].rolling(window = ADXwindow,
                                center=False).sum()
temp['AverageTrueRange'] = ((temp['AverageTrueRange'].shift(1)*(ADXwindow-1
                             ) + temp['TrueRange']) / ADXwindow)
temp['PDM'] = (temp['High'] - temp['High'].shift(1))
temp['MDM'] = (temp['Low'].shift(1) - temp['Low'])
temp['PDM'] = temp['PDM'][temp['PDM'] > 0]
temp['MDM'] = temp['MDM'][temp['MDM'] > 0]
temp['PDM'] = temp['PDM'].fillna(0)
temp['MDM'] = temp['MDM'].fillna(0)
temp['SmoothPDM'] = temp['PDM'].rolling(window = ADXwindow,
                                center=False).sum()
temp['SmoothPDM'] = ((temp['SmoothPDM'].shift(1)*(ADXwindow-1
                             ) + temp['PDM']) / ADXwindow)
temp['SmoothMDM'] = temp['MDM'].rolling(window = ADXwindow,
                                center=False).sum()
temp['SmoothMDM'] = ((temp['SmoothMDM'].shift(1)*(ADXwindow-1
                             ) + temp['MDM']) / ADXwindow)
temp['PDI'] = (100*(temp['SmoothPDM']/temp['AverageTrueRange']))
temp['MDI'] = (100*(temp['SmoothMDM']/temp['AverageTrueRange']))
temp['DIdiff'] = abs(temp['PDI'] - temp['MDI'])
temp['DIsum'] = temp['PDI'] + temp['MDI']
temp['DX'] = (100 * (temp['DIdiff']/temp['DIsum']))
temp['ADX'] = temp['DX'].rolling(window = ADXwindow, center = False).mean()
temp['DIdivergence'] = temp['PDI'] - temp['MDI']
temp['ADXMean'] = temp['ADX'].mean() * .9 #Scaling factor
temp['ADXStrength'] = temp['ADX']/temp['ADXMean']

#Ballerbands Lower/Upperband, bandwidth, b%
BBwindow = 20
temp['nDaySMA'] = temp['Adj Close'].rolling(window=BBwindow, center=False).mean()
temp['nDaySTD'] = temp['Adj Close'].rolling(window=BBwindow, center=False).std()
temp['UpperBand'] = temp['nDaySMA'] + (temp['nDaySTD'] * 2)
temp['LowerBand'] = temp['nDaySMA'] - (temp['nDaySTD'] * 2)
temp['BandWidth'] = ((temp['UpperBand'] - temp['LowerBand'])/temp['nDaySMA'])*100
temp['B'] = (temp['Adj Close'] - temp['LowerBand'])/(temp['UpperBand'] - temp['LowerBand'])

#Chaikin Money Flow MFMultiplier, CMF (CMF - need to normalize or make rolling sum)
CMFwindow = 20
temp['MFMultiplier'] = (((temp['Adj Close'] - temp['Low']) - (temp['High'] 
- temp['Adj Close'])) / (temp['High'] - temp['Low']))
temp['MFVolume'] = (temp['Volume'] * temp['MFMultiplier'])
temp['ZeroLine'] = 0
temp['CMF'] = temp['MFVolume'].rolling(center=False, window=CMFwindow).sum(
        )/temp['Volume'].rolling(center=False, window=CMFwindow).sum()

#Commodity Channel Index
constant = .02
CCIwindow = 20 
temp['TP'] = (temp['High'] + temp['Low'] + temp['Adj Close']) / 3
temp['TPSMA'] = temp['TP'].rolling(center=False, window = CCIwindow).mean()
temp['MeanDeviation'] = temp['TP'].rolling(center=False, window = CCIwindow).std()
temp['CCI'] = ((temp['TP'] - temp['TPSMA'])/(constant*temp['MeanDeviation']))
temp['Top'] = 100
temp['Bottom'] = -100

#Day over average rolling volume DayOverARV
DayOverwindow = 60
temp['AverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                    window=DayOverwindow).mean() 
temp['DayOverARV'] = temp['Volume']/temp['AverageRollingVolume'] 

#Simple Moving Average
littlewindow = 20 #number of days for moving average window
bigwindow = 252 #numer of days for moving average window
temp['SmallSMA'] = temp['Adj Close'].rolling(window=littlewindow, center=False).mean()
temp['LargeSMA'] = temp['Adj Close'].rolling(window=bigwindow, center=False).mean()
temp['4wkOver52wk'] = (temp['SmallSMA'] - temp['LargeSMA'])/temp['Adj Close']
temp['priceOver4wk'] = (temp['Adj Close'] - temp['SmallSMA'])/temp['Adj Close']
#RSI
closeprice = temp['Adj Close']
RSIwindow = 14  
change = closeprice.diff()
change = change[1:]
up, down = change.copy(), change.copy()
up[up < 0] = 0
down[down > 0] = 0
AvgGain = up.rolling(RSIwindow).mean()
AvgGain = AvgGain.fillna(0)
AvgLoss = down.abs().rolling(RSIwindow).mean()
AvgLoss = AvgLoss.fillna(0)
RS = AvgGain/AvgLoss
RS = RS.fillna(0)
RSI = 100 - (100/(1.0+RS))
temp['RSI'] = pd.Series(RSI)

#Gap Up
temp['GapUp'] = (temp['High'].shift(1) - temp['Low']) / temp['Adj Close'].shift(1)
temp['GapUp'] = temp['GapUp'][temp['GapUp'] < 0]
temp['GapUp'] = temp['GapUp'].fillna(0)
temp['GapUp'] = np.where(temp['GapUp'] == 0 , 0, (-1*temp['GapUp']))

#Gap Down
temp['GapDown'] = (temp['Low'].shift(1) - temp['High']) / temp['Adj Close'].shift(1)
temp['GapDown'] = temp['GapDown'][temp['GapDown'] > 0]
temp['GapDown'] = temp['GapDown'].fillna(0)

#Rate of Change
lag = 12
temp['RateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(lag)
                                  ) / temp['Adj Close'].shift(lag)        
        
