# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 10:35:04 2017

@author: AmatVictoriaCuramIII
"""
import pandas as pd
import time as t
from datetime import date
import datetime
import os
import numpy as np
start = t.time()

DatabaseTickers = os.listdir('F:\\Users\\AmatVictoriaCuram\\Database')

DatabaseCSV = [s + '.csv' for s in DatabaseTickers]

ranger = range(0,len(DatabaseCSV))

for i in ranger:
    try:
        temp = pd.read_pickle('F:\\Users\\AmatVictoriaCuram\\Database\\' +
            DatabaseCSV[i][:-4]+ '\\' + DatabaseCSV[i][:-4])
            
        for x in temp.columns:
            temp[x] =  pd.to_numeric(temp[x], errors='coerce')

        ranger2 = range(0,len(temp['Adj Close']))
        index = temp.index            
        #LogReturns  
        temp['LogRet'] = np.log(temp['Adj Close']/temp['Adj Close'].shift(1)) 
        temp['LogRet'] = temp['LogRet'].fillna(0)
        #Min/Max
        temp['AllTimeLow'] = temp['Adj Close'].min()
        temp['AllTimeHigh'] = temp['Adj Close'].max()
        temp['52wkLow'] = temp['Adj Close'].rolling(252).min()
        temp['52wkHigh'] = temp['Adj Close'].rolling(252).max()
        temp['11wkLow'] = temp['Adj Close'].rolling(55).min()
        temp['11wkHigh'] = temp['Adj Close'].rolling(55).max()
        temp['4wkLow'] = temp['Adj Close'].rolling(20).min()
        temp['4wkHigh'] = temp['Adj Close'].rolling(20).max()
        #B/O, B/D
        temp['52wkBreakOutRatio'] = temp['High']/temp['52wkHigh'] #If > 1, then moving higher
        temp['52wkBreakDownRatio'] = temp['52wkLow']/temp['Low'] #If > 1, then moving lower
        #Days listed
        temp['Age'] = len(temp['Open'])
        #Over all time, the average return per period
        temp['TotalAverage52wkReturn'] = temp['LogRet'].mean() * 252  
        temp['TotalAverage52wkStdDev'] = temp['LogRet'].std(
                                                             )*np.sqrt(252)
        temp['TotalAverage11wkReturn'] = temp['LogRet'].mean() * 55
        temp['TotalAverage11wkStdDev'] = temp['LogRet'].std(
                                                             )*np.sqrt(55)
        temp['TotalAverage4wkReturn'] = temp['LogRet'].mean() * 20
        temp['TotalAverage4wkStdDev'] = temp['LogRet'].std(
                                                             )*np.sqrt(20)
        #CV Annual only
        temp['CoefficientOfVaration'] = (
        temp['TotalAverage52wkStdDev']/temp['TotalAverage52wkReturn'])
        #Over rolling period, Average return during period
        temp['Rolling52wkAverageReturn'] = temp['LogRet'].rolling(
                                         center=False, window = 252).mean()
        temp['Rolling11wkAverageReturn'] = temp['LogRet'].rolling(
                                         center=False, window = 55).mean()
        temp['Rolling4wkAverageReturn'] = temp['LogRet'].rolling(
                                         center=False, window = 20).mean()
        #Over rolling period, Average Std Dev during period
        temp['Rolling52wkStdDev'] = temp['LogRet'].rolling(
                                        center = False, window = 252).std()
        temp['Rolling11wkStdDev'] = temp['LogRet'].rolling(
                                         center = False, window = 55).std()        
        temp['Rolling4wkStdDev'] = temp['LogRet'].rolling(
                                         center = False, window = 20).std()
        #%CHG from period
        temp['Rolling52wkReturn'] = np.log(temp['Adj Close']/
                                             temp['Adj Close'].shift(252))
        temp['Rolling11wkReturn'] = np.log(temp['Adj Close']/
                                             temp['Adj Close'].shift(55))
        temp['Rolling4wkReturn'] = np.log(temp['Adj Close']/
                                             temp['Adj Close'].shift(20))
        #Over rolling period Average volume in period
        temp['RollingAverage52wkVolume'] = temp['Volume'].rolling(
                                           center=False, window=252).mean()
        temp['RollingAverage11wkVolume'] = temp['Volume'].rolling(
                                           center=False, window=55).mean()
        temp['RollingAverage4wkVolume'] = temp['Volume'].rolling(
                                           center=False, window=20).mean()

        #Front period over Average Stats
        temp['Rolling52wkReturnOverAverage'] = (temp['Rolling52wkAverageReturn']/ 
                                                temp['TotalAverage52wkReturn'])
        temp['Rolling11wkReturnOverAverage'] = (temp['Rolling11wkAverageReturn']/ 
                                                temp['TotalAverage11wkReturn'])
        temp['Rolling4wkReturnOverAverage'] =  (temp['Rolling4wkAverageReturn']/ 
                                                temp['TotalAverage4wkReturn'])
                                                
        temp['Rolling52wkStdDevOverAverage'] = (temp['Rolling52wkStdDev']/ 
                                                temp['TotalAverage52wkStdDev'])
        temp['Rolling11wkStdDevOverAverage'] = (temp['Rolling11wkStdDev']/ 
                                                temp['TotalAverage11wkStdDev'])
        temp['Rolling4wkStdDevOverAverage'] =  (temp['Rolling4wkStdDev']/ 
                                                temp['TotalAverage4wkStdDev'])
        temp['AverageOverRolling52wkStdDev'] = (temp['TotalAverage52wkStdDev']/
                                                temp['Rolling52wkStdDev'])
        temp['AverageOverRolling11wkStdDev'] = (temp['TotalAverage11wkStdDev']/
                                                temp['Rolling11wkStdDev'])
        temp['AverageOverRolling4wkStdDev'] =  (temp['TotalAverage4wkStdDev']/
                                                temp['Rolling4wkStdDev'])
        #Gap Up
        temp['GapUp'] = (temp['High'].shift(1) - temp['Low']) / temp['Adj Close'].shift(1)
        temp['GapUp'] = temp['GapUp'][temp['GapUp'] < 0]
        temp['GapUp'] = temp['GapUp'].fillna(0)
        temp['GapUp'] = np.where(temp['GapUp'] == 0 , 0, (-1*temp['GapUp']))
        #Gap Down
        temp['GapDown'] = (temp['Low'].shift(1) - temp['High']) / temp['Adj Close'].shift(1)
        temp['GapDown'] = temp['GapDown'][temp['GapDown'] > 0]
        temp['GapDown'] = temp['GapDown'].fillna(0)
        #ATR calculation
        ATRwindow = 20
        temp['Method1'] = temp['High'] - temp['Low']
        temp['Method2'] = abs((temp['High'] - temp['Adj Close'].shift(1)))
        temp['Method3'] = abs((temp['Low'] - temp['Adj Close'].shift(1)))
        temp['Method1'] = temp['Method1'].fillna(0)
        temp['Method2'] = temp['Method2'].fillna(0)
        temp['Method3'] = temp['Method3'].fillna(0)
        temp['TrueRange'] = temp[['Method1','Method2','Method3']].max(axis = 1)
        temp['SumTrueRange'] = temp['TrueRange'].rolling(window = ATRwindow,
                                        center=False).sum()
        temp['SumTrueRange'] = temp['SumTrueRange'].fillna(0)
        temp['AverageTrueRangePoints'] = temp['SumTrueRange']/ATRwindow
        temp['AverageTrueRangePercent'] = (temp['AverageTrueRangePoints']/
                                            temp['Adj Close'])
        #60 day efficiency
        EFwindow = 60                                             
        temp['ATR'] = temp['TrueRange'].rolling(window = EFwindow,
                                center=False).mean()
        temp['CloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(EFwindow)
        temp['Efficiency'] = temp['CloseDiff'] / temp['ATR']                                        
        #Day over average rolling volume DayOverARV
        ARVWindow = 20
        temp['AverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                            window=ARVWindow).mean() 
        temp['VolumeOverAverage'] = temp['Volume']/(temp['AverageRollingVolume']) 
        #Simple Moving Average
        littlewindow = 20 #number of days for moving average window
        middlewindow = 55        
        bigwindow = 252 #numer of days for moving average window
        temp['4wkSMA'] = temp['Adj Close'].rolling(window=littlewindow, center=False).mean()
        temp['4wkSMA'] = temp['4wkSMA'].fillna(0)
        temp['11wkSMA'] = temp['Adj Close'].rolling(window=middlewindow, center=False).mean()
        temp['11wkSMA'] = temp['11wkSMA'].fillna(0)        
        temp['52wkSMA'] = temp['Adj Close'].rolling(window=bigwindow, center=False).mean()
        temp['52wkSMA'] = temp['52wkSMA'].fillna(0)
        #All stats in % based on close price
        temp['priceOver4wk'] = (temp['Adj Close'] - temp['4wkSMA'])/temp['Adj Close']   
        temp['priceOver4wk'] = temp['priceOver4wk'].fillna(0)
        temp['priceOver11wk'] = (temp['Adj Close'] - temp['11wkSMA'])/temp['Adj Close']
        temp['priceOver11wk'] = temp['priceOver11wk'].fillna(0)        
        temp['priceOver52wk'] = (temp['Adj Close'] - temp['52wkSMA'])/temp['Adj Close']
        temp['priceOver52wk'] = temp['priceOver52wk'].fillna(0)
        temp['4wkOver52wk'] = (temp['4wkSMA'] - temp['52wkSMA'])/temp['Adj Close']
        temp['4wkOver52wk'] = temp['4wkOver52wk'].fillna(0)                
        temp['4wkOver11wk'] = (temp['4wkSMA'] - temp['11wkSMA'])/temp['Adj Close']
        temp['4wkOver11wk'] = temp['4wkOver11wk'].fillna(0)
        temp['11wkOver52wk'] = (temp['11wkSMA'] - temp['52wkSMA'])/temp['Adj Close']
        temp['11wkOver52wk'] = temp['11wkOver52wk'].fillna(0)
        #Rate of Change - 20 day
        lag = 20
        temp['RateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(lag)
                                          ) / temp['Adj Close'].shift(lag)  
        temp['RateOfChange'] = temp['RateOfChange'].fillna(0)
#            
#        #drop column function
#        temp = temp.drop(['Age','AverageAnnualReturn','AverageAnnualRollingVolume',
#               'AnnualStandardDeviation','CoefficientOfVaration',
#               'CoefficientOfVaration', '4wkOver52wkStandardDeviationRatio'],
#                axis = 1) #drop column function
        
        temp = temp[~temp.index.duplicated(keep='first')]
        
        pd.to_pickle(temp, 'F:\\Users\\AmatVictoriaCuram\\Database\\' +
                        DatabaseCSV[i][:-4] + '\\' + DatabaseCSV[i][:-4])
    except OSError:
        continue
    except ValueError:
        continue
end = t.time()
print('Whole update took ', str(end - start), 'seconds.')