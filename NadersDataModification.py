# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 10:35:04 2017

@author: AmatVictoriaCuramIII
"""
import pandas as pd
from pandas import read_csv
import time as t
#from datetime import date
#import datetime
import os
#import numpy as np
start = t.time()

DatabaseTickers = os.listdir('F:\\Users\\AmatVictoriaCuram\\NadersData')

DatabaseCSV = [s + '.csv' for s in DatabaseTickers]

ranger = range(0,len(DatabaseCSV))

#Load the CSV
QualitativeData = read_csv('C:\\Users\\AmatVictoriaCuramIII\\Desktop\\Python\\PretrimQualitativeData.csv', sep = ',')
QualitativeDataTickers = list(QualitativeData['Symbol'])
#See what time series need qualitative data
ExistingPickles = os.listdir('F:\\Users\\AmatVictoriaCuram\\NadersData')

#A gorgeous list comprehension that delivers all tickers in QualitativeData 
#that have a corresponding time series in existing library
CommonList = [x for x in ExistingPickles if x in QualitativeDataTickers]

#for every issue in common, assign each individual qualitative data value as vector
for i in CommonList:
    try:
#        Access Qualitative Data row and pull out data to add to pickle
        QualitativeDataRow = QualitativeData[QualitativeData['Symbol'] == i]
        temp = pd.read_pickle('F:\\Users\\AmatVictoriaCuram\\NadersData\\' + i + '\\' + i)
#Force Numeric... Keep nearby, TURNS ALL STR to NAN
#        for x in temp.columns:
#            temp[x] =  pd.to_numeric(temp[x], errors='coerce') 
        temp['Ticker'] = i #type = string
        temp['Name'] = QualitativeDataRow.iloc[0][1]
        temp['LastSale'] = float(QualitativeDataRow.iloc[0][2])
        temp['GivenMarketCap'] = QualitativeDataRow.iloc[0][3]
#        temp['ADRTSO'] = QualitativeDataRow.iloc[0][4]
        temp['IPOyear'] = QualitativeDataRow.iloc[0][5]
        temp['Sector'] = QualitativeDataRow.iloc[0][6]
        temp['Industry'] = QualitativeDataRow.iloc[0][7]
#        temp['SummaryQuote'] = QualitativeDataRow.iloc[0][8]
        temp['SharesOutstanding'] = temp['GivenMarketCap']/temp['LastSale']
        temp['MarketCap'] = (temp['SharesOutstanding'] * temp['Adj Close'])/10**9
                  
        #Basic Date information
        temp['Age'] = len(temp['Adj Close'])
        temp['Year'] = temp.index.year
        temp['Month'] = temp.index.month
        temp['Day'] = temp.index.day
        temp['DayOfWeek'] = temp.index.dayofweek
        
        #Index column for main database
#        temp['TickerDate'] = i + temp['Year'].astype(str) + temp['Month'].astype(str) + temp['Day'].astype(str)
        #Daily Log Returns
        temp['CloseToClose'] = (temp['Adj Close']/temp['Adj Close'].shift(1) - 1)
        temp['CloseToClose'] = temp['CloseToClose'].fillna(0)
        temp['OpenToOpen'] = (temp['Open']/temp['Open'].shift(1) - 1)
        temp['OpenToOpen'] = temp['OpenToOpen'].fillna(0)
        temp['CloseToOpen'] = (temp['Open']/temp['Adj Close'].shift(1) - 1)
        temp['CloseToOpen'] = temp['CloseToOpen'].fillna(0)   
        temp['OpenToClose'] = (temp['Adj Close']/temp['Open'] - 1) 
        temp['OpenToClose'] = temp['OpenToClose'].fillna(0) 
        #Shifted Returns - Open, High, Low, Close
        temp['ShiftedOpen'] = temp['Open'].shift(1)
        temp['ShiftedOpen'] = temp['ShiftedOpen'].fillna(0) 
        temp['ShiftedHigh'] = temp['High'].shift(1)
        temp['ShiftedHigh'] = temp['ShiftedHigh'].fillna(0)         
        temp['ShiftedLow'] = temp['Low'].shift(1)
        temp['ShiftedLow'] = temp['ShiftedLow'].fillna(0)
        temp['ShiftedClose'] = temp['Close'].shift(1)
        temp['ShiftedClose'] = temp['ShiftedClose'].fillna(0)    
        temp['ShiftedAdjClose'] = temp['Adj Close'].shift(1)
        temp['ShiftedAdjClose'] = temp['ShiftedAdjClose'].fillna(0) 
        
#                #drop column function
#        temp = temp.drop(['Column','List'], axis = 1) #drop column function
        temp = temp[~temp.index.duplicated(keep='first')]
        pd.to_pickle(temp, 'F:\\Users\\AmatVictoriaCuram\\NadersData\\' + i + '\\' + i)
        print(i)
    except OSError:
        continue
    except ValueError:
        continue
end = t.time()
print('Whole update took ', str(end - start), 'seconds.')
#for i in ranger:
#    try:
#        print(DatabaseCSV[i])
#        temp = pd.read_pickle('F:\\Users\\AmatVictoriaCuram\\NadersData\\' +
#            DatabaseCSV[i][:-4]+ '\\' + DatabaseCSV[i][:-4])
#            
#        for x in temp.columns:
#            temp[x] =  pd.to_numeric(temp[x], errors='coerce')                   
#        #Basic Date information
#        temp['Age'] = len(temp['Adj Close'])
#        temp['Year'] = temp.index.year
#        temp['Month'] = temp.index.month
#        temp['Day'] = temp.index.day
#        temp['DayOfWeek'] = temp.index.dayofweek
##        #Daily Log Returns
#        temp['CloseToClose'] = temp['Adj Close']/temp['Adj Close'].shift(1)
#        temp['CloseToClose'] = temp['CloseToClose'].fillna(1)
#        temp['OpenToOpen'] = temp['Open']/temp['Open'].shift(1)
#        temp['OpenToOpen'] = temp['OpenToOpen'].fillna(1)
#        temp['CloseToOpen'] = temp['Open']/temp['Adj Close'].shift(1)
#        temp['CloseToOpen'] = temp['CloseToOpen'].fillna(1)
#        temp['LogRet'] = np.log(temp['Adj Close']/temp['Adj Close'].shift(1)) 
#        temp['LogRet'] = temp['LogRet'].fillna(0)
#        #Min/Max & RangePoints/RangePercent
#        temp['AllTimeLow'] = temp['Adj Close'].min()
#        temp['AllTimeHigh'] = temp['Adj Close'].max()
#        temp['100wkLow'] = temp['Adj Close'].rolling(500).min()
#        temp['100wkHigh'] = temp['Adj Close'].rolling(500).max()
#        temp['100wkRangePoints'] = temp['100wkHigh'] - temp['100wkLow']
#        temp['100wkRangePercent'] = temp['100wkRangePoints'] / temp['Adj Close']
#        temp['90wkLow'] = temp['Adj Close'].rolling(450).min()
#        temp['90wkHigh'] = temp['Adj Close'].rolling(450).max()
#        temp['90wkRangePoints'] = temp['90wkHigh'] - temp['90wkLow']
#        temp['90wkRangePercent'] = temp['90wkRangePoints'] / temp['Adj Close']
#        temp['80wkLow'] = temp['Adj Close'].rolling(400).min()
#        temp['80wkHigh'] = temp['Adj Close'].rolling(400).max()
#        temp['80wkRangePoints'] = temp['80wkHigh'] - temp['80wkLow']
#        temp['80wkRangePercent'] = temp['80wkRangePoints'] / temp['Adj Close']
#        temp['70wkLow'] = temp['Adj Close'].rolling(350).min()
#        temp['70wkHigh'] = temp['Adj Close'].rolling(350).max()
#        temp['70wkRangePoints'] = temp['70wkHigh'] - temp['70wkLow']
#        temp['70wkRangePercent'] = temp['70wkRangePoints'] / temp['Adj Close']
#        temp['65wkLow'] = temp['Adj Close'].rolling(325).min()
#        temp['65wkHigh'] = temp['Adj Close'].rolling(325).max()
#        temp['65wkRangePoints'] = temp['65wkHigh'] - temp['65wkLow']
#        temp['65wkRangePercent'] = temp['65wkRangePoints'] / temp['Adj Close']
#        temp['60wkLow'] = temp['Adj Close'].rolling(300).min()
#        temp['60wkHigh'] = temp['Adj Close'].rolling(300).max()
#        temp['60wkRangePoints'] = temp['60wkHigh'] - temp['60wkLow']
#        temp['60wkRangePercent'] = temp['60wkRangePoints'] / temp['Adj Close']
#        temp['55wkLow'] = temp['Adj Close'].rolling(275).min()
#        temp['55wkHigh'] = temp['Adj Close'].rolling(275).max()
#        temp['55wkRangePoints'] = temp['55wkHigh'] - temp['55wkLow']
#        temp['55wkRangePercent'] = temp['55wkRangePoints'] / temp['Adj Close']
#        temp['52wkLow'] = temp['Adj Close'].rolling(252).min()
#        temp['52wkHigh'] = temp['Adj Close'].rolling(252).max()
#        temp['52wkRangePoints'] = temp['52wkHigh'] - temp['52wkLow']
#        temp['52wkRangePercent'] = temp['52wkRangePoints'] / temp['Adj Close']
#        temp['45wkLow'] = temp['Adj Close'].rolling(225).min()
#        temp['45wkHigh'] = temp['Adj Close'].rolling(225).max()
#        temp['45wkRangePoints'] = temp['45wkHigh'] - temp['45wkLow']
#        temp['45wkRangePercent'] = temp['45wkRangePoints'] / temp['Adj Close']
#        temp['40wkLow'] = temp['Adj Close'].rolling(200).min()
#        temp['40wkHigh'] = temp['Adj Close'].rolling(200).max()
#        temp['40wkRangePoints'] = temp['40wkHigh'] - temp['40wkLow']
#        temp['40wkRangePercent'] = temp['40wkRangePoints'] / temp['Adj Close']
#        temp['35wkLow'] = temp['Adj Close'].rolling(175).min()
#        temp['35wkHigh'] = temp['Adj Close'].rolling(175).max()
#        temp['35wkRangePoints'] = temp['35wkHigh'] - temp['35wkLow']
#        temp['35wkRangePercent'] = temp['35wkRangePoints'] / temp['Adj Close']
#        temp['30wkLow'] = temp['Adj Close'].rolling(150).min()
#        temp['30wkHigh'] = temp['Adj Close'].rolling(150).max()
#        temp['30wkRangePoints'] = temp['30wkHigh'] - temp['30wkLow']
#        temp['30wkRangePercent'] = temp['30wkRangePoints'] / temp['Adj Close']
#        temp['25wkLow'] = temp['Adj Close'].rolling(125).min()
#        temp['25wkHigh'] = temp['Adj Close'].rolling(125).max()
#        temp['25wkRangePoints'] = temp['25wkHigh'] - temp['25wkLow']
#        temp['25wkRangePercent'] = temp['25wkRangePoints'] / temp['Adj Close']
#        temp['20wkLow'] = temp['Adj Close'].rolling(100).min()
#        temp['20wkHigh'] = temp['Adj Close'].rolling(100).max()
#        temp['20wkRangePoints'] = temp['20wkHigh'] - temp['20wkLow']
#        temp['20wkRangePercent'] = temp['20wkRangePoints'] / temp['Adj Close']
#        temp['15wkLow'] = temp['Adj Close'].rolling(75).min()
#        temp['15wkHigh'] = temp['Adj Close'].rolling(75).max()
#        temp['15wkRangePoints'] = temp['15wkHigh'] - temp['15wkLow']
#        temp['15wkRangePercent'] = temp['15wkRangePoints'] / temp['Adj Close']
#        temp['12wkLow'] = temp['Adj Close'].rolling(60).min()
#        temp['12wkHigh'] = temp['Adj Close'].rolling(60).max()
#        temp['12wkRangePoints'] = temp['12wkHigh'] - temp['12wkLow']
#        temp['12wkRangePercent'] = temp['12wkRangePoints'] / temp['Adj Close']
#        temp['11wkLow'] = temp['Adj Close'].rolling(55).min()
#        temp['11wkHigh'] = temp['Adj Close'].rolling(55).max()
#        temp['11wkRangePoints'] = temp['11wkHigh'] - temp['11wkLow']
#        temp['11wkRangePercent'] = temp['11wkRangePoints'] / temp['Adj Close']
#        temp['10wkLow'] = temp['Adj Close'].rolling(50).min()
#        temp['10wkHigh'] = temp['Adj Close'].rolling(50).max()
#        temp['10wkRangePoints'] = temp['10wkHigh'] - temp['10wkLow']
#        temp['10wkRangePercent'] = temp['10wkRangePoints'] / temp['Adj Close']
#        temp['9wkLow'] = temp['Adj Close'].rolling(45).min()
#        temp['9wkHigh'] = temp['Adj Close'].rolling(45).max()
#        temp['9wkRangePoints'] = temp['9wkHigh'] - temp['9wkLow']
#        temp['9wkRangePercent'] = temp['9wkRangePoints'] / temp['Adj Close']
#        temp['8wkLow'] = temp['Adj Close'].rolling(40).min()
#        temp['8wkHigh'] = temp['Adj Close'].rolling(40).max()
#        temp['8wkRangePoints'] = temp['8wkHigh'] - temp['8wkLow']
#        temp['8wkRangePercent'] = temp['8wkRangePoints'] / temp['Adj Close']
#        temp['7wkLow'] = temp['Adj Close'].rolling(35).min()
#        temp['7wkHigh'] = temp['Adj Close'].rolling(35).max()
#        temp['7wkRangePoints'] = temp['7wkHigh'] - temp['7wkLow']
#        temp['7wkRangePercent'] = temp['7wkRangePoints'] / temp['Adj Close']
#        temp['6wkLow'] = temp['Adj Close'].rolling(30).min()
#        temp['6wkHigh'] = temp['Adj Close'].rolling(30).max()
#        temp['6wkRangePoints'] = temp['6wkHigh'] - temp['6wkLow']
#        temp['6wkRangePercent'] = temp['6wkRangePoints'] / temp['Adj Close']
#        temp['5wkLow'] = temp['Adj Close'].rolling(25).min()
#        temp['5wkHigh'] = temp['Adj Close'].rolling(25).max()
#        temp['5wkRangePoints'] = temp['5wkHigh'] - temp['5wkLow']
#        temp['5wkRangePercent'] = temp['5wkRangePoints'] / temp['Adj Close']
#        temp['4wkLow'] = temp['Adj Close'].rolling(20).min()
#        temp['4wkHigh'] = temp['Adj Close'].rolling(20).max()
#        temp['4wkRangePoints'] = temp['4wkHigh'] - temp['4wkLow']
#        temp['4wkRangePercent'] = temp['4wkRangePoints'] / temp['Adj Close']   
#        temp['3wkLow'] = temp['Adj Close'].rolling(15).min()
#        temp['3wkHigh'] = temp['Adj Close'].rolling(15).max()
#        temp['3wkRangePoints'] = temp['3wkHigh'] - temp['3wkLow']
#        temp['3wkRangePercent'] = temp['3wkRangePoints'] / temp['Adj Close']
#        temp['2wkLow'] = temp['Adj Close'].rolling(10).min()
#        temp['2wkHigh'] = temp['Adj Close'].rolling(10).max()
#        temp['2wkRangePoints'] = temp['2wkHigh'] - temp['2wkLow']
#        temp['2wkRangePercent'] = temp['2wkRangePoints'] / temp['Adj Close']
#        temp['1wkLow'] = temp['Adj Close'].rolling(5).min()
#        temp['1wkHigh'] = temp['Adj Close'].rolling(5).max()
#        temp['1wkRangePoints'] = temp['1wkHigh'] - temp['1wkLow']
#        temp['1wkRangePercent'] = temp['1wkRangePoints'] / temp['Adj Close']
#        temp['4dayLow'] = temp['Adj Close'].rolling(4).min()
#        temp['4dayHigh'] = temp['Adj Close'].rolling(4).max()
#        temp['4dayRangePoints'] = temp['4dayHigh'] - temp['4dayLow']
#        temp['4dayRangePercent'] = temp['4dayRangePoints'] / temp['Adj Close']
#        temp['3dayLow'] = temp['Adj Close'].rolling(3).min()
#        temp['3dayHigh'] = temp['Adj Close'].rolling(3).max()
#        temp['3dayRangePoints'] = temp['3dayHigh'] - temp['3dayLow']
#        temp['3dayRangePercent'] = temp['3dayRangePoints'] / temp['Adj Close']
#        temp['2dayLow'] = temp['Adj Close'].rolling(2).min()
#        temp['2dayHigh'] = temp['Adj Close'].rolling(2).max()
#        temp['2dayRangePoints'] = temp['2dayHigh'] - temp['2dayLow']
#        temp['2dayRangePercent'] = temp['2dayRangePoints'] / temp['Adj Close']
#
#        #B/O, B/D ratio
#        temp['100wkBreakOutRatio'] = temp['High']/temp['100wkHigh'] #If > 1, then moving higher
#        temp['100wkBreakDownRatio'] = temp['Low']/temp['100wkLow'] #If > 1, then moving lower
#        temp['90wkBreakOutRatio'] = temp['High']/temp['90wkHigh'] #If > 1, then moving higher
#        temp['90wkBreakDownRatio'] = temp['Low']/temp['90wkLow'] #If > 1, then moving lower
#        temp['80wkBreakOutRatio'] = temp['High']/temp['80wkHigh'] #If > 1, then moving higher
#        temp['80wkBreakDownRatio'] = temp['Low']/temp['80wkLow'] #If > 1, then moving lower
#        temp['70wkBreakOutRatio'] = temp['High']/temp['70wkHigh'] #If > 1, then moving higher
#        temp['70wkBreakDownRatio'] = temp['Low']/temp['70wkLow'] #If > 1, then moving lower
#        temp['65wkBreakOutRatio'] = temp['High']/temp['65wkHigh'] #If > 1, then moving higher
#        temp['65wkBreakDownRatio'] = temp['Low']/temp['65wkLow'] #If > 1, then moving lower
#        temp['60wkBreakOutRatio'] = temp['High']/temp['60wkHigh'] #If > 1, then moving higher
#        temp['60wkBreakDownRatio'] = temp['Low']/temp['60wkLow'] #If > 1, then moving lower
#        temp['55wkBreakOutRatio'] = temp['High']/temp['55wkHigh'] #If > 1, then moving higher
#        temp['55wkBreakDownRatio'] = temp['Low']/temp['55wkLow'] #If > 1, then moving lower
#        temp['52wkBreakOutRatio'] = temp['High']/temp['52wkHigh'] #If > 1, then moving higher
#        temp['52wkBreakDownRatio'] = temp['Low']/temp['52wkLow'] #If > 1, then moving lower
#        temp['45wkBreakOutRatio'] = temp['High']/temp['45wkHigh'] #If > 1, then moving higher
#        temp['45wkBreakDownRatio'] = temp['Low']/temp['45wkLow'] #If > 1, then moving lower
#        temp['40wkBreakOutRatio'] = temp['High']/temp['40wkHigh'] #If > 1, then moving higher
#        temp['40wkBreakDownRatio'] = temp['Low']/temp['40wkLow'] #If > 1, then moving lower
#        temp['35wkBreakOutRatio'] = temp['High']/temp['35wkHigh'] #If > 1, then moving higher
#        temp['35wkBreakDownRatio'] = temp['Low']/temp['35wkLow'] #If > 1, then moving lower
#        temp['30wkBreakOutRatio'] = temp['High']/temp['30wkHigh'] #If > 1, then moving higher
#        temp['30wkBreakDownRatio'] = temp['Low']/temp['30wkLow'] #If > 1, then moving lower
#        temp['25wkBreakOutRatio'] = temp['High']/temp['25wkHigh'] #If > 1, then moving higher
#        temp['25wkBreakDownRatio'] = temp['Low']/temp['25wkLow'] #If > 1, then moving lower
#        temp['20wkBreakOutRatio'] = temp['High']/temp['20wkHigh'] #If > 1, then moving higher
#        temp['20wkBreakDownRatio'] = temp['Low']/temp['20wkLow'] #If > 1, then moving lower
#        temp['15wkBreakOutRatio'] = temp['High']/temp['15wkHigh'] #If > 1, then moving higher
#        temp['15wkBreakDownRatio'] = temp['Low']/temp['15wkLow'] #If > 1, then moving lower
#        temp['12wkBreakOutRatio'] = temp['High']/temp['12wkHigh'] #If > 1, then moving higher
#        temp['12wkBreakDownRatio'] = temp['Low']/temp['12wkLow'] #If > 1, then moving lower
#        temp['11wkBreakOutRatio'] = temp['High']/temp['11wkHigh'] #If > 1, then moving higher
#        temp['11wkBreakDownRatio'] = temp['Low']/temp['11wkLow'] #If > 1, then moving lower
#        temp['10wkBreakOutRatio'] = temp['High']/temp['10wkHigh'] #If > 1, then moving higher
#        temp['10wkBreakDownRatio'] = temp['Low']/temp['10wkLow'] #If > 1, then moving lower
#        temp['9wkBreakOutRatio'] = temp['High']/temp['9wkHigh'] #If > 1, then moving higher
#        temp['9wkBreakDownRatio'] = temp['Low']/temp['9wkLow'] #If > 1, then moving lower
#        temp['8wkBreakOutRatio'] = temp['High']/temp['8wkHigh'] #If > 1, then moving higher
#        temp['8wkBreakDownRatio'] = temp['Low']/temp['8wkLow'] #If > 1, then moving lower
#        temp['7wkBreakOutRatio'] = temp['High']/temp['7wkHigh'] #If > 1, then moving higher
#        temp['7wkBreakDownRatio'] = temp['Low']/temp['7wkLow'] #If > 1, then moving lower
#        temp['6wkBreakOutRatio'] = temp['High']/temp['6wkHigh'] #If > 1, then moving higher
#        temp['6wkBreakDownRatio'] = temp['Low']/temp['6wkLow'] #If > 1, then moving lower
#        temp['5wkBreakOutRatio'] = temp['High']/temp['5wkHigh'] #If > 1, then moving higher
#        temp['5wkBreakDownRatio'] = temp['Low']/temp['5wkLow'] #If > 1, then moving lower
#        temp['4wkBreakOutRatio'] = temp['High']/temp['4wkHigh'] #If > 1, then moving higher
#        temp['4wkBreakDownRatio'] = temp['Low']/temp['4wkLow'] #If > 1, then moving lower
#        temp['3wkBreakOutRatio'] = temp['High']/temp['3wkHigh'] #If > 1, then moving higher
#        temp['3wkBreakDownRatio'] = temp['Low']/temp['3wkLow'] #If > 1, then moving lower
#        temp['2wkBreakOutRatio'] = temp['High']/temp['2wkHigh'] #If > 1, then moving higher
#        temp['2wkBreakDownRatio'] = temp['Low']/temp['2wkLow'] #If > 1, then moving lower
#        temp['1wkBreakOutRatio'] = temp['High']/temp['1wkHigh'] #If > 1, then moving higher
#        temp['1wkBreakDownRatio'] = temp['Low']/temp['1wkLow'] #If > 1, then moving lower
#        temp['4dayBreakOutRatio'] = temp['High']/temp['4dayHigh'] #If > 1, then moving higher
#        temp['4dayBreakDownRatio'] = temp['Low']/temp['4dayLow'] #If > 1, then moving lower
#        temp['3dayBreakOutRatio'] = temp['High']/temp['3dayHigh'] #If > 1, then moving higher
#        temp['3dayBreakDownRatio'] = temp['Low']/temp['3dayLow'] #If > 1, then moving lower
#        temp['2dayBreakOutRatio'] = temp['High']/temp['2dayHigh'] #If > 1, then moving higher
#        temp['2dayBreakDownRatio'] = temp['Low']/temp['2dayLow'] #If > 1, then moving lower
#
#        #Over all time, the average return per period
#        temp['TotalAverage52wkReturn'] = temp['LogRet'].mean() * 252  
#        temp['TotalAverage52wkStdDev'] = temp['LogRet'].std()*np.sqrt(252)
#        temp['TotalAverage11wkReturn'] = temp['LogRet'].mean() * 55
#        temp['TotalAverage11wkStdDev'] = temp['LogRet'].std()*np.sqrt(55)
#        temp['TotalAverage4wkReturn'] = temp['LogRet'].mean() * 20
#        temp['TotalAverage4wkStdDev'] = temp['LogRet'].std()*np.sqrt(20)
#        #CV Annual only
#        temp['CoefficientOfVaration'] = (
#        temp['TotalAverage52wkStdDev']/temp['TotalAverage52wkReturn'])
#        #Over rolling period, Average return during period
#        temp['Rolling52wkAverageReturn'] = temp['LogRet'].rolling(
#                                         center=False, window = 252).mean()
#        temp['Rolling11wkAverageReturn'] = temp['LogRet'].rolling(
#                                         center=False, window = 55).mean()
#        temp['Rolling4wkAverageReturn'] = temp['LogRet'].rolling(
#                                         center=False, window = 20).mean()
#        #Over rolling period, Average Std Dev during period
#        temp['Rolling52wkStdDev'] = temp['LogRet'].rolling(
#                                        center = False, window = 252).std()
#        temp['Rolling11wkStdDev'] = temp['LogRet'].rolling(
#                                         center = False, window = 55).std()        
#        temp['Rolling4wkStdDev'] = temp['LogRet'].rolling(
#                                         center = False, window = 20).std()
#        #%CHG from period
#        temp['Rolling52wkReturn'] = np.log(temp['Adj Close']/
#                                             temp['Adj Close'].shift(252))
#        temp['Rolling11wkReturn'] = np.log(temp['Adj Close']/
#                                             temp['Adj Close'].shift(55))
#        temp['Rolling4wkReturn'] = np.log(temp['Adj Close']/
#                                             temp['Adj Close'].shift(20))
#        #Over rolling period Average volume in period
#        temp['RollingAverage52wkVolume'] = temp['Volume'].rolling(
#                                           center=False, window=252).mean()
#        temp['RollingAverage11wkVolume'] = temp['Volume'].rolling(
#                                           center=False, window=55).mean()
#        temp['RollingAverage4wkVolume'] = temp['Volume'].rolling(
#                                           center=False, window=20).mean()
#
#        #Front period over Average Stats
#        temp['Rolling52wkReturnOverAverage'] = (temp['Rolling52wkAverageReturn']/ 
#                                                temp['TotalAverage52wkReturn'])
#        temp['Rolling11wkReturnOverAverage'] = (temp['Rolling11wkAverageReturn']/ 
#                                                temp['TotalAverage11wkReturn'])
#        temp['Rolling4wkReturnOverAverage'] =  (temp['Rolling4wkAverageReturn']/ 
#                                                temp['TotalAverage4wkReturn'])
#                                                
#        temp['Rolling52wkStdDevOverAverage'] = (temp['Rolling52wkStdDev']/ 
#                                                temp['TotalAverage52wkStdDev'])
#        temp['Rolling11wkStdDevOverAverage'] = (temp['Rolling11wkStdDev']/ 
#                                                temp['TotalAverage11wkStdDev'])
#        temp['Rolling4wkStdDevOverAverage'] =  (temp['Rolling4wkStdDev']/ 
#                                                temp['TotalAverage4wkStdDev'])
#        temp['AverageOverRolling52wkStdDev'] = (temp['TotalAverage52wkStdDev']/
#                                                temp['Rolling52wkStdDev'])
#        temp['AverageOverRolling11wkStdDev'] = (temp['TotalAverage11wkStdDev']/
#                                                temp['Rolling11wkStdDev'])
#        temp['AverageOverRolling4wkStdDev'] =  (temp['TotalAverage4wkStdDev']/
#                                                temp['Rolling4wkStdDev'])
#        #Gap Up
#        temp['GapUp'] = (temp['High'].shift(1) - temp['Low']) / temp['Adj Close'].shift(1)
#        temp['GapUp'] = temp['GapUp'][temp['GapUp'] < 0]
#        temp['GapUp'] = temp['GapUp'].fillna(0)
#        temp['GapUp'] = np.where(temp['GapUp'] == 0 , 0, (-1*temp['GapUp']))
#        #Gap Down
#        temp['GapDown'] = (temp['Low'].shift(1) - temp['High']) / temp['Adj Close'].shift(1)
#        temp['GapDown'] = temp['GapDown'][temp['GapDown'] > 0]
#        temp['GapDown'] = temp['GapDown'].fillna(0)
#        #ATR calculation
#        ATRwindow = 20
#        temp['Method1'] = temp['High'] - temp['Low']
#        temp['Method2'] = abs((temp['High'] - temp['Adj Close'].shift(1)))
#        temp['Method3'] = abs((temp['Low'] - temp['Adj Close'].shift(1)))
#        temp['Method1'] = temp['Method1'].fillna(0)
#        temp['Method2'] = temp['Method2'].fillna(0)
#        temp['Method3'] = temp['Method3'].fillna(0)
#        temp['TrueRange'] = temp[['Method1','Method2','Method3']].max(axis = 1)
#        temp['SumTrueRange'] = temp['TrueRange'].rolling(window = ATRwindow,
#                                        center=False).sum()
#        temp['SumTrueRange'] = temp['SumTrueRange'].fillna(0)
#        temp['AverageTrueRangePoints'] = temp['SumTrueRange']/ATRwindow
#        temp['AverageTrueRangePercent'] = (temp['AverageTrueRangePoints']/
#                                            temp['Adj Close'])
#        
#        #60 day efficiency
#        EFwindow = 60                                             
#        temp['ATR'] = temp['TrueRange'].rolling(window = EFwindow,
#                                center=False).mean()
#        temp['CloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(EFwindow)
#        temp['Efficiency'] = temp['CloseDiff'] / temp['ATR']                                        
#        #Day over average rolling volume DayOverARV
#        ARVWindow = 20
#        temp['AverageRollingVolume'] = temp['Volume'].rolling(center=False, 
#                                                            window=ARVWindow).mean() 
#        temp['VolumeOverAverage'] = temp['Volume']/(temp['AverageRollingVolume']) 
#        #Simple Moving Average
#        littlewindow = 20 #number of days for moving average window
#        middlewindow = 55        
#        bigwindow = 252 #numer of days for moving average window
#        temp['4wkSMA'] = temp['Adj Close'].rolling(window=littlewindow, center=False).mean()
#        temp['4wkSMA'] = temp['4wkSMA'].fillna(0)
#        temp['11wkSMA'] = temp['Adj Close'].rolling(window=middlewindow, center=False).mean()
#        temp['11wkSMA'] = temp['11wkSMA'].fillna(0)        
#        temp['52wkSMA'] = temp['Adj Close'].rolling(window=bigwindow, center=False).mean()
#        temp['52wkSMA'] = temp['52wkSMA'].fillna(0)
#        #All stats in % based on close price
#        temp['priceOver4wk'] = (temp['Adj Close'] - temp['4wkSMA'])/temp['Adj Close']   
#        temp['priceOver4wk'] = temp['priceOver4wk'].fillna(0)
#        temp['priceOver11wk'] = (temp['Adj Close'] - temp['11wkSMA'])/temp['Adj Close']
#        temp['priceOver11wk'] = temp['priceOver11wk'].fillna(0)        
#        temp['priceOver52wk'] = (temp['Adj Close'] - temp['52wkSMA'])/temp['Adj Close']
#        temp['priceOver52wk'] = temp['priceOver52wk'].fillna(0)
#        temp['4wkOver52wk'] = (temp['4wkSMA'] - temp['52wkSMA'])/temp['Adj Close']
#        temp['4wkOver52wk'] = temp['4wkOver52wk'].fillna(0)                
#        temp['4wkOver11wk'] = (temp['4wkSMA'] - temp['11wkSMA'])/temp['Adj Close']
#        temp['4wkOver11wk'] = temp['4wkOver11wk'].fillna(0)
#        temp['11wkOver52wk'] = (temp['11wkSMA'] - temp['52wkSMA'])/temp['Adj Close']
#        temp['11wkOver52wk'] = temp['11wkOver52wk'].fillna(0)
#        #Rate of Change - 20 day
#        lag = 20
#        temp['RateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(lag)
#                                          ) / temp['Adj Close'].shift(lag)  
#        temp['RateOfChange'] = temp['RateOfChange'].fillna(0)
#            
#        #drop column function
#        temp = temp.drop(['Age','AverageAnnualReturn','AverageAnnualRollingVolume',
#               'AnnualStandardDeviation','CoefficientOfVaration',
#               'CoefficientOfVaration', '4wkOver52wkStandardDeviationRatio'],
#                axis = 1) #drop column function
        
#        temp = temp[~temp.index.duplicated(keep='first')]
#        
#        pd.to_pickle(temp, 'F:\\Users\\AmatVictoriaCuram\\Database\\' +
#                        DatabaseCSV[i][:-4] + '\\' + DatabaseCSV[i][:-4])
#    except OSError:
#        continue
#    except ValueError:
#        continue
