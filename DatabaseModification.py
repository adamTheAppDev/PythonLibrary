# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 10:35:04 2017

@author: AmatVictoriaCuramIII
"""
#The power comes from within you
import pandas as pd
import time as t
#from datetime import date
#import datetime
import os
import numpy as np
start = t.time()

DatabaseTickers = os.listdir('F:\\Users\\AmatVictoriaCuram\\Database')

DatabaseCSV = [s + '.csv' for s in DatabaseTickers]

ranger = range(0,len(DatabaseCSV))

for i in ranger:
    try:
        print(DatabaseCSV[i])
        temp = pd.read_pickle('F:\\Users\\AmatVictoriaCuram\\Database\\' +
            DatabaseCSV[i][:-4]+ '\\' + DatabaseCSV[i][:-4])
        #Are the next two lines necessary?
        for x in temp.columns:
            temp[x] =  pd.to_numeric(temp[x], errors='coerce')                   
        #Basic Date information
        temp['Age'] = len(temp['Adj Close'])
        temp['Year'] = temp.index.year
        temp['Month'] = temp.index.month
        temp['Day'] = temp.index.day
        temp['DayOfWeek'] = temp.index.dayofweek
        #Daily Log Returns
        temp['LogRet'] = np.log(temp['Adj Close']/temp['Adj Close'].shift(1)) 
        temp['LogRet'] = temp['LogRet'].fillna(0)
        #Min/Max & RangePoints/RangePercent
        temp['AllTimeLow'] = temp['Adj Close'].min()
        temp['AllTimeHigh'] = temp['Adj Close'].max()
        temp['100wkLow'] = temp['Adj Close'].rolling(500).min()
        temp['100wkHigh'] = temp['Adj Close'].rolling(500).max()
        temp['100wkRangePoints'] = temp['100wkHigh'] - temp['100wkLow']
        temp['100wkRangePercent'] = temp['100wkRangePoints'] / temp['Adj Close']
        temp['90wkLow'] = temp['Adj Close'].rolling(450).min()
        temp['90wkHigh'] = temp['Adj Close'].rolling(450).max()
        temp['90wkRangePoints'] = temp['90wkHigh'] - temp['90wkLow']
        temp['90wkRangePercent'] = temp['90wkRangePoints'] / temp['Adj Close']
        temp['80wkLow'] = temp['Adj Close'].rolling(400).min()
        temp['80wkHigh'] = temp['Adj Close'].rolling(400).max()
        temp['80wkRangePoints'] = temp['80wkHigh'] - temp['80wkLow']
        temp['80wkRangePercent'] = temp['80wkRangePoints'] / temp['Adj Close']
        temp['70wkLow'] = temp['Adj Close'].rolling(350).min()
        temp['70wkHigh'] = temp['Adj Close'].rolling(350).max()
        temp['70wkRangePoints'] = temp['70wkHigh'] - temp['70wkLow']
        temp['70wkRangePercent'] = temp['70wkRangePoints'] / temp['Adj Close']
        temp['65wkLow'] = temp['Adj Close'].rolling(325).min()
        temp['65wkHigh'] = temp['Adj Close'].rolling(325).max()
        temp['65wkRangePoints'] = temp['65wkHigh'] - temp['65wkLow']
        temp['65wkRangePercent'] = temp['65wkRangePoints'] / temp['Adj Close']
        temp['60wkLow'] = temp['Adj Close'].rolling(300).min()
        temp['60wkHigh'] = temp['Adj Close'].rolling(300).max()
        temp['60wkRangePoints'] = temp['60wkHigh'] - temp['60wkLow']
        temp['60wkRangePercent'] = temp['60wkRangePoints'] / temp['Adj Close']
        temp['55wkLow'] = temp['Adj Close'].rolling(275).min()
        temp['55wkHigh'] = temp['Adj Close'].rolling(275).max()
        temp['55wkRangePoints'] = temp['55wkHigh'] - temp['55wkLow']
        temp['55wkRangePercent'] = temp['55wkRangePoints'] / temp['Adj Close']
        temp['52wkLow'] = temp['Adj Close'].rolling(252).min()
        temp['52wkHigh'] = temp['Adj Close'].rolling(252).max()
        temp['52wkRangePoints'] = temp['52wkHigh'] - temp['52wkLow']
        temp['52wkRangePercent'] = temp['52wkRangePoints'] / temp['Adj Close']
        temp['45wkLow'] = temp['Adj Close'].rolling(225).min()
        temp['45wkHigh'] = temp['Adj Close'].rolling(225).max()
        temp['45wkRangePoints'] = temp['45wkHigh'] - temp['45wkLow']
        temp['45wkRangePercent'] = temp['45wkRangePoints'] / temp['Adj Close']
        temp['40wkLow'] = temp['Adj Close'].rolling(200).min()
        temp['40wkHigh'] = temp['Adj Close'].rolling(200).max()
        temp['40wkRangePoints'] = temp['40wkHigh'] - temp['40wkLow']
        temp['40wkRangePercent'] = temp['40wkRangePoints'] / temp['Adj Close']
        temp['35wkLow'] = temp['Adj Close'].rolling(175).min()
        temp['35wkHigh'] = temp['Adj Close'].rolling(175).max()
        temp['35wkRangePoints'] = temp['35wkHigh'] - temp['35wkLow']
        temp['35wkRangePercent'] = temp['35wkRangePoints'] / temp['Adj Close']
        temp['30wkLow'] = temp['Adj Close'].rolling(150).min()
        temp['30wkHigh'] = temp['Adj Close'].rolling(150).max()
        temp['30wkRangePoints'] = temp['30wkHigh'] - temp['30wkLow']
        temp['30wkRangePercent'] = temp['30wkRangePoints'] / temp['Adj Close']
        temp['25wkLow'] = temp['Adj Close'].rolling(125).min()
        temp['25wkHigh'] = temp['Adj Close'].rolling(125).max()
        temp['25wkRangePoints'] = temp['25wkHigh'] - temp['25wkLow']
        temp['25wkRangePercent'] = temp['25wkRangePoints'] / temp['Adj Close']
        temp['20wkLow'] = temp['Adj Close'].rolling(100).min()
        temp['20wkHigh'] = temp['Adj Close'].rolling(100).max()
        temp['20wkRangePoints'] = temp['20wkHigh'] - temp['20wkLow']
        temp['20wkRangePercent'] = temp['20wkRangePoints'] / temp['Adj Close']
        temp['15wkLow'] = temp['Adj Close'].rolling(75).min()
        temp['15wkHigh'] = temp['Adj Close'].rolling(75).max()
        temp['15wkRangePoints'] = temp['15wkHigh'] - temp['15wkLow']
        temp['15wkRangePercent'] = temp['15wkRangePoints'] / temp['Adj Close']
        temp['12wkLow'] = temp['Adj Close'].rolling(60).min()
        temp['12wkHigh'] = temp['Adj Close'].rolling(60).max()
        temp['12wkRangePoints'] = temp['12wkHigh'] - temp['12wkLow']
        temp['12wkRangePercent'] = temp['12wkRangePoints'] / temp['Adj Close']
        temp['11wkLow'] = temp['Adj Close'].rolling(55).min()
        temp['11wkHigh'] = temp['Adj Close'].rolling(55).max()
        temp['11wkRangePoints'] = temp['11wkHigh'] - temp['11wkLow']
        temp['11wkRangePercent'] = temp['11wkRangePoints'] / temp['Adj Close']
        temp['10wkLow'] = temp['Adj Close'].rolling(50).min()
        temp['10wkHigh'] = temp['Adj Close'].rolling(50).max()
        temp['10wkRangePoints'] = temp['10wkHigh'] - temp['10wkLow']
        temp['10wkRangePercent'] = temp['10wkRangePoints'] / temp['Adj Close']
        temp['9wkLow'] = temp['Adj Close'].rolling(45).min()
        temp['9wkHigh'] = temp['Adj Close'].rolling(45).max()
        temp['9wkRangePoints'] = temp['9wkHigh'] - temp['9wkLow']
        temp['9wkRangePercent'] = temp['9wkRangePoints'] / temp['Adj Close']
        temp['8wkLow'] = temp['Adj Close'].rolling(40).min()
        temp['8wkHigh'] = temp['Adj Close'].rolling(40).max()
        temp['8wkRangePoints'] = temp['8wkHigh'] - temp['8wkLow']
        temp['8wkRangePercent'] = temp['8wkRangePoints'] / temp['Adj Close']
        temp['7wkLow'] = temp['Adj Close'].rolling(35).min()
        temp['7wkHigh'] = temp['Adj Close'].rolling(35).max()
        temp['7wkRangePoints'] = temp['7wkHigh'] - temp['7wkLow']
        temp['7wkRangePercent'] = temp['7wkRangePoints'] / temp['Adj Close']
        temp['6wkLow'] = temp['Adj Close'].rolling(30).min()
        temp['6wkHigh'] = temp['Adj Close'].rolling(30).max()
        temp['6wkRangePoints'] = temp['6wkHigh'] - temp['6wkLow']
        temp['6wkRangePercent'] = temp['6wkRangePoints'] / temp['Adj Close']
        temp['5wkLow'] = temp['Adj Close'].rolling(25).min()
        temp['5wkHigh'] = temp['Adj Close'].rolling(25).max()
        temp['5wkRangePoints'] = temp['5wkHigh'] - temp['5wkLow']
        temp['5wkRangePercent'] = temp['5wkRangePoints'] / temp['Adj Close']
        temp['4wkLow'] = temp['Adj Close'].rolling(20).min()
        temp['4wkHigh'] = temp['Adj Close'].rolling(20).max()
        temp['4wkRangePoints'] = temp['4wkHigh'] - temp['4wkLow']
        temp['4wkRangePercent'] = temp['4wkRangePoints'] / temp['Adj Close']   
        temp['3wkLow'] = temp['Adj Close'].rolling(15).min()
        temp['3wkHigh'] = temp['Adj Close'].rolling(15).max()
        temp['3wkRangePoints'] = temp['3wkHigh'] - temp['3wkLow']
        temp['3wkRangePercent'] = temp['3wkRangePoints'] / temp['Adj Close']
        temp['2wkLow'] = temp['Adj Close'].rolling(10).min()
        temp['2wkHigh'] = temp['Adj Close'].rolling(10).max()
        temp['2wkRangePoints'] = temp['2wkHigh'] - temp['2wkLow']
        temp['2wkRangePercent'] = temp['2wkRangePoints'] / temp['Adj Close']
        temp['1wkLow'] = temp['Adj Close'].rolling(5).min()
        temp['1wkHigh'] = temp['Adj Close'].rolling(5).max()
        temp['1wkRangePoints'] = temp['1wkHigh'] - temp['1wkLow']
        temp['1wkRangePercent'] = temp['1wkRangePoints'] / temp['Adj Close']
        temp['4dayLow'] = temp['Adj Close'].rolling(4).min()
        temp['4dayHigh'] = temp['Adj Close'].rolling(4).max()
        temp['4dayRangePoints'] = temp['4dayHigh'] - temp['4dayLow']
        temp['4dayRangePercent'] = temp['4dayRangePoints'] / temp['Adj Close']
        temp['3dayLow'] = temp['Adj Close'].rolling(3).min()
        temp['3dayHigh'] = temp['Adj Close'].rolling(3).max()
        temp['3dayRangePoints'] = temp['3dayHigh'] - temp['3dayLow']
        temp['3dayRangePercent'] = temp['3dayRangePoints'] / temp['Adj Close']
        temp['2dayLow'] = temp['Adj Close'].rolling(2).min()
        temp['2dayHigh'] = temp['Adj Close'].rolling(2).max()
        temp['2dayRangePoints'] = temp['2dayHigh'] - temp['2dayLow']
        temp['2dayRangePercent'] = temp['2dayRangePoints'] / temp['Adj Close']

        #B/O, B/D ratio
        temp['100wkBreakOutRatio'] = temp['High']/temp['100wkHigh'] #If > 1, then moving higher
        temp['100wkBreakDownRatio'] = temp['Low']/temp['100wkLow'] #If > 1, then moving lower
        temp['90wkBreakOutRatio'] = temp['High']/temp['90wkHigh'] #If > 1, then moving higher
        temp['90wkBreakDownRatio'] = temp['Low']/temp['90wkLow'] #If > 1, then moving lower
        temp['80wkBreakOutRatio'] = temp['High']/temp['80wkHigh'] #If > 1, then moving higher
        temp['80wkBreakDownRatio'] = temp['Low']/temp['80wkLow'] #If > 1, then moving lower
        temp['70wkBreakOutRatio'] = temp['High']/temp['70wkHigh'] #If > 1, then moving higher
        temp['70wkBreakDownRatio'] = temp['Low']/temp['70wkLow'] #If > 1, then moving lower
        temp['65wkBreakOutRatio'] = temp['High']/temp['65wkHigh'] #If > 1, then moving higher
        temp['65wkBreakDownRatio'] = temp['Low']/temp['65wkLow'] #If > 1, then moving lower
        temp['60wkBreakOutRatio'] = temp['High']/temp['60wkHigh'] #If > 1, then moving higher
        temp['60wkBreakDownRatio'] = temp['Low']/temp['60wkLow'] #If > 1, then moving lower
        temp['55wkBreakOutRatio'] = temp['High']/temp['55wkHigh'] #If > 1, then moving higher
        temp['55wkBreakDownRatio'] = temp['Low']/temp['55wkLow'] #If > 1, then moving lower
        temp['52wkBreakOutRatio'] = temp['High']/temp['52wkHigh'] #If > 1, then moving higher
        temp['52wkBreakDownRatio'] = temp['Low']/temp['52wkLow'] #If > 1, then moving lower
        temp['45wkBreakOutRatio'] = temp['High']/temp['45wkHigh'] #If > 1, then moving higher
        temp['45wkBreakDownRatio'] = temp['Low']/temp['45wkLow'] #If > 1, then moving lower
        temp['40wkBreakOutRatio'] = temp['High']/temp['40wkHigh'] #If > 1, then moving higher
        temp['40wkBreakDownRatio'] = temp['Low']/temp['40wkLow'] #If > 1, then moving lower
        temp['35wkBreakOutRatio'] = temp['High']/temp['35wkHigh'] #If > 1, then moving higher
        temp['35wkBreakDownRatio'] = temp['Low']/temp['35wkLow'] #If > 1, then moving lower
        temp['30wkBreakOutRatio'] = temp['High']/temp['30wkHigh'] #If > 1, then moving higher
        temp['30wkBreakDownRatio'] = temp['Low']/temp['30wkLow'] #If > 1, then moving lower
        temp['25wkBreakOutRatio'] = temp['High']/temp['25wkHigh'] #If > 1, then moving higher
        temp['25wkBreakDownRatio'] = temp['Low']/temp['25wkLow'] #If > 1, then moving lower
        temp['20wkBreakOutRatio'] = temp['High']/temp['20wkHigh'] #If > 1, then moving higher
        temp['20wkBreakDownRatio'] = temp['Low']/temp['20wkLow'] #If > 1, then moving lower
        temp['15wkBreakOutRatio'] = temp['High']/temp['15wkHigh'] #If > 1, then moving higher
        temp['15wkBreakDownRatio'] = temp['Low']/temp['15wkLow'] #If > 1, then moving lower
        temp['12wkBreakOutRatio'] = temp['High']/temp['12wkHigh'] #If > 1, then moving higher
        temp['12wkBreakDownRatio'] = temp['Low']/temp['12wkLow'] #If > 1, then moving lower
        temp['11wkBreakOutRatio'] = temp['High']/temp['11wkHigh'] #If > 1, then moving higher
        temp['11wkBreakDownRatio'] = temp['Low']/temp['11wkLow'] #If > 1, then moving lower
        temp['10wkBreakOutRatio'] = temp['High']/temp['10wkHigh'] #If > 1, then moving higher
        temp['10wkBreakDownRatio'] = temp['Low']/temp['10wkLow'] #If > 1, then moving lower
        temp['9wkBreakOutRatio'] = temp['High']/temp['9wkHigh'] #If > 1, then moving higher
        temp['9wkBreakDownRatio'] = temp['Low']/temp['9wkLow'] #If > 1, then moving lower
        temp['8wkBreakOutRatio'] = temp['High']/temp['8wkHigh'] #If > 1, then moving higher
        temp['8wkBreakDownRatio'] = temp['Low']/temp['8wkLow'] #If > 1, then moving lower
        temp['7wkBreakOutRatio'] = temp['High']/temp['7wkHigh'] #If > 1, then moving higher
        temp['7wkBreakDownRatio'] = temp['Low']/temp['7wkLow'] #If > 1, then moving lower
        temp['6wkBreakOutRatio'] = temp['High']/temp['6wkHigh'] #If > 1, then moving higher
        temp['6wkBreakDownRatio'] = temp['Low']/temp['6wkLow'] #If > 1, then moving lower
        temp['5wkBreakOutRatio'] = temp['High']/temp['5wkHigh'] #If > 1, then moving higher
        temp['5wkBreakDownRatio'] = temp['Low']/temp['5wkLow'] #If > 1, then moving lower
        temp['4wkBreakOutRatio'] = temp['High']/temp['4wkHigh'] #If > 1, then moving higher
        temp['4wkBreakDownRatio'] = temp['Low']/temp['4wkLow'] #If > 1, then moving lower
        temp['3wkBreakOutRatio'] = temp['High']/temp['3wkHigh'] #If > 1, then moving higher
        temp['3wkBreakDownRatio'] = temp['Low']/temp['3wkLow'] #If > 1, then moving lower
        temp['2wkBreakOutRatio'] = temp['High']/temp['2wkHigh'] #If > 1, then moving higher
        temp['2wkBreakDownRatio'] = temp['Low']/temp['2wkLow'] #If > 1, then moving lower
        temp['1wkBreakOutRatio'] = temp['High']/temp['1wkHigh'] #If > 1, then moving higher
        temp['1wkBreakDownRatio'] = temp['Low']/temp['1wkLow'] #If > 1, then moving lower
        temp['4dayBreakOutRatio'] = temp['High']/temp['4dayHigh'] #If > 1, then moving higher
        temp['4dayBreakDownRatio'] = temp['Low']/temp['4dayLow'] #If > 1, then moving lower
        temp['3dayBreakOutRatio'] = temp['High']/temp['3dayHigh'] #If > 1, then moving higher
        temp['3dayBreakDownRatio'] = temp['Low']/temp['3dayLow'] #If > 1, then moving lower
        temp['2dayBreakOutRatio'] = temp['High']/temp['2dayHigh'] #If > 1, then moving higher
        temp['2dayBreakDownRatio'] = temp['Low']/temp['2dayLow'] #If > 1, then moving lower

        #Over all time, the average return per period & average Std Dev per period; STATIC
        temp['100wkTotalAverageReturn'] = temp['LogRet'].mean() * 500 
        temp['100wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(500)
        temp['90wkTotalAverageReturn'] = temp['LogRet'].mean() * 450
        temp['90wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(450)
        temp['80wkTotalAverageReturn'] = temp['LogRet'].mean() * 400
        temp['80wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(400)
        temp['70wkTotalAverageReturn'] = temp['LogRet'].mean() * 350
        temp['70wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(350)
        temp['65wkTotalAverageReturn'] = temp['LogRet'].mean() * 325
        temp['65wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(325)        
        temp['60wkTotalAverageReturn'] = temp['LogRet'].mean() * 300
        temp['60wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(300)
        temp['55wkTotalAverageReturn'] = temp['LogRet'].mean() * 275
        temp['55wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(275)
        temp['52wkTotalAverageReturn'] = temp['LogRet'].mean() * 252
        temp['52wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(252)
        temp['45wkTotalAverageReturn'] = temp['LogRet'].mean() * 225
        temp['45wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(225)
        temp['40wkTotalAverageReturn'] = temp['LogRet'].mean() * 200
        temp['40wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(200)
        temp['35wkTotalAverageReturn'] = temp['LogRet'].mean() * 175
        temp['35wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(175)
        temp['30wkTotalAverageReturn'] = temp['LogRet'].mean() * 150
        temp['30wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(150)
        temp['25wkTotalAverageReturn'] = temp['LogRet'].mean() * 125
        temp['25wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(125)
        temp['20wkTotalAverageReturn'] = temp['LogRet'].mean() * 100
        temp['20wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(100)
        temp['15wkTotalAverageReturn'] = temp['LogRet'].mean() * 75
        temp['15wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(75)
        temp['12wkTotalAverageReturn'] = temp['LogRet'].mean() * 60
        temp['12wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(60)
        temp['11wkTotalAverageReturn'] = temp['LogRet'].mean() * 55
        temp['11wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(55)
        temp['10wkTotalAverageReturn'] = temp['LogRet'].mean() * 50
        temp['10wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(50)
        temp['9wkTotalAverageReturn'] = temp['LogRet'].mean() * 45
        temp['9wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(45)
        temp['8wkTotalAverageReturn'] = temp['LogRet'].mean() * 40
        temp['8wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(40)
        temp['7wkTotalAverageReturn'] = temp['LogRet'].mean() * 35
        temp['7wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(35)
        temp['6wkTotalAverageReturn'] = temp['LogRet'].mean() * 30
        temp['6wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(30)
        temp['5wkTotalAverageReturn'] = temp['LogRet'].mean() * 25
        temp['5wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(25)
        temp['4wkTotalAverageReturn'] = temp['LogRet'].mean() * 20
        temp['4wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(20)
        temp['3wkTotalAverageReturn'] = temp['LogRet'].mean() * 15
        temp['3wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(15)
        temp['2wkTotalAverageReturn'] = temp['LogRet'].mean() * 10
        temp['2wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(10)
        temp['1wkTotalAverageReturn'] = temp['LogRet'].mean() * 5
        temp['1wkTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(5)
        temp['4dayTotalAverageReturn'] = temp['LogRet'].mean() * 4
        temp['4dayTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(4)
        temp['3dayTotalAverageReturn'] = temp['LogRet'].mean() * 3
        temp['3dayTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(3)
        temp['2dayTotalAverageReturn'] = temp['LogRet'].mean() * 2
        temp['2dayTotalAverageStdDev'] = temp['LogRet'].std()*np.sqrt(2)
        
        #CV IS STATIC = not rolling
        temp['100wkCoefficientOfVaration'] = (
                temp['100wkTotalAverageStdDev']/temp['100wkTotalAverageReturn'])
        temp['90wkCoefficientOfVaration'] = (
                temp['90wkTotalAverageStdDev']/temp['90wkTotalAverageReturn'])
        temp['80wkCoefficientOfVaration'] = (
                temp['80wkTotalAverageStdDev']/temp['80wkTotalAverageReturn'])
        temp['70wkCoefficientOfVaration'] = (
                temp['70wkTotalAverageStdDev']/temp['70wkTotalAverageReturn'])
        temp['65wkCoefficientOfVaration'] = (
                temp['65wkTotalAverageStdDev']/temp['65wkTotalAverageReturn'])
        temp['60wkCoefficientOfVaration'] = (
                temp['60wkTotalAverageStdDev']/temp['60wkTotalAverageReturn'])
        temp['55wkCoefficientOfVaration'] = (
                temp['55wkTotalAverageStdDev']/temp['55wkTotalAverageReturn'])
        temp['52wkCoefficientOfVaration'] = (
                temp['52wkTotalAverageStdDev']/temp['52wkTotalAverageReturn'])
        temp['45wkCoefficientOfVaration'] = (
                temp['45wkTotalAverageStdDev']/temp['45wkTotalAverageReturn'])
        temp['40wkCoefficientOfVaration'] = (
                temp['40wkTotalAverageStdDev']/temp['40wkTotalAverageReturn'])
        temp['35wkCoefficientOfVaration'] = (
                temp['35wkTotalAverageStdDev']/temp['35wkTotalAverageReturn'])
        temp['30wkCoefficientOfVaration'] = (
                temp['30wkTotalAverageStdDev']/temp['30wkTotalAverageReturn'])
        temp['25wkCoefficientOfVaration'] = (
                temp['25wkTotalAverageStdDev']/temp['25wkTotalAverageReturn'])
        temp['20wkCoefficientOfVaration'] = (
                temp['20wkTotalAverageStdDev']/temp['20wkTotalAverageReturn'])
        temp['15wkCoefficientOfVaration'] = (
                temp['15wkTotalAverageStdDev']/temp['15wkTotalAverageReturn'])
        temp['12CoefficientOfVaration'] = (
                temp['12wkTotalAverageStdDev']/temp['12wkTotalAverageReturn'])
        temp['11wkCoefficientOfVaration'] = (
                temp['11wkTotalAverageStdDev']/temp['11wkTotalAverageReturn'])
        temp['10wkCoefficientOfVaration'] = (
                temp['10wkTotalAverageStdDev']/temp['10wkTotalAverageReturn'])
        temp['9wkCoefficientOfVaration'] = (
                temp['9wkTotalAverageStdDev']/temp['9wkTotalAverageReturn'])
        temp['8wkCoefficientOfVaration'] = (
                temp['8wkTotalAverageStdDev']/temp['8wkTotalAverageReturn'])
        temp['7wkCoefficientOfVaration'] = (
                temp['7wkTotalAverageStdDev']/temp['7wkTotalAverageReturn'])
        temp['6wkCoefficientOfVaration'] = (
                temp['6wkTotalAverageStdDev']/temp['6wkTotalAverageReturn'])
        temp['5wkCoefficientOfVaration'] = (
                temp['5wkTotalAverageStdDev']/temp['5wkTotalAverageReturn'])
        temp['4wkCoefficientOfVaration'] = (
                temp['4wkTotalAverageStdDev']/temp['4wkTotalAverageReturn'])
        temp['3wkCoefficientOfVaration'] = (
                temp['3wkTotalAverageStdDev']/temp['3wkTotalAverageReturn'])
        temp['2wkCoefficientOfVaration'] = (
                temp['2wkTotalAverageStdDev']/temp['2wkTotalAverageReturn'])
        temp['1wkCoefficientOfVaration'] = (
                temp['1wkTotalAverageStdDev']/temp['1wkTotalAverageReturn'])
        temp['4dayCoefficientOfVaration'] = (
                temp['4dayTotalAverageStdDev']/temp['4dayTotalAverageReturn'])
        temp['3dayCoefficientOfVaration'] = (
                temp['3dayTotalAverageStdDev']/temp['3dayTotalAverageReturn'])
        temp['2dayCoefficientOfVaration'] = (
                temp['2dayTotalAverageStdDev']/temp['2dayTotalAverageReturn'])
                
        #Over rolling period, Average return during period; DYNAMIC
        temp['100wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                         center=False, window = 500).mean()
        temp['90wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                         center=False, window = 450).mean()                                         
        temp['80wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                         center=False, window = 400).mean()
        temp['70wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                         center=False, window = 350).mean()
        temp['65wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                         center=False, window = 325).mean()   
        temp['60wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                         center=False, window = 300).mean()
        temp['55wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                         center=False, window = 275).mean()
        temp['52wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                         center=False, window = 252).mean()
        temp['45wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                         center=False, window = 225).mean()
        temp['40wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                         center=False, window = 200).mean()
        temp['35wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                         center=False, window = 175).mean()
        temp['30wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                         center=False, window = 150).mean()
        temp['25wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                         center=False, window = 125).mean()
        temp['20wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                         center=False, window = 100).mean()
        temp['15wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                         center=False, window = 75).mean()
        temp['12wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                         center=False, window = 60).mean()
        temp['11wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                         center=False, window = 55).mean()
        temp['10wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                         center=False, window = 50).mean()
        temp['9wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                         center=False, window = 45).mean()
        temp['8wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                         center=False, window = 40).mean()
        temp['7wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                         center=False, window = 35).mean()
        temp['6wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                         center=False, window = 30).mean()
        temp['5wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                         center=False, window = 25).mean()                                         
        temp['4wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                         center=False, window = 20).mean()
        temp['3wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                         center=False, window = 15).mean()
        temp['2wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                         center=False, window = 10).mean()
        temp['1wkRollingAverageReturn'] = temp['LogRet'].rolling(
                                         center=False, window = 5).mean()
        temp['4dayRollingAverageReturn'] = temp['LogRet'].rolling(
                                         center=False, window = 4).mean()
        temp['3dayRollingAverageReturn'] = temp['LogRet'].rolling(
                                         center=False, window = 3).mean()
        temp['2dayRollingAverageReturn'] = temp['LogRet'].rolling(
                                         center=False, window = 2).mean()                                         
                                         
                                         
        #Over rolling period, Average Std Dev during period; DYNAMIC
        temp['100wkRollingStdDev'] = temp['LogRet'].rolling(
                                         center=False, window = 500).std()
        temp['90wkRollingStdDev'] = temp['LogRet'].rolling(
                                         center=False, window = 450).std()                                         
        temp['80wkRollingStdDev'] = temp['LogRet'].rolling(
                                         center=False, window = 400).std()
        temp['70wkRollingStdDev'] = temp['LogRet'].rolling(
                                         center=False, window = 350).std()
        temp['65wkRollingStdDev'] = temp['LogRet'].rolling(
                                         center=False, window = 325).std()   
        temp['60wkRollingStdDev'] = temp['LogRet'].rolling(
                                         center=False, window = 300).std()
        temp['55wkRollingStdDev'] = temp['LogRet'].rolling(
                                         center=False, window = 275).std()
        temp['52wkRollingStdDev'] = temp['LogRet'].rolling(
                                         center=False, window = 252).std()
        temp['45wkRollingStdDev'] = temp['LogRet'].rolling(
                                         center=False, window = 225).std()
        temp['40wkRollingStdDev'] = temp['LogRet'].rolling(
                                         center=False, window = 200).std()
        temp['35wkRollingStdDev'] = temp['LogRet'].rolling(
                                         center=False, window = 175).std()
        temp['30wkRollingStdDev'] = temp['LogRet'].rolling(
                                         center=False, window = 150).std()
        temp['25wkRollingStdDev'] = temp['LogRet'].rolling(
                                         center=False, window = 125).std()
        temp['20wkRollingStdDev'] = temp['LogRet'].rolling(
                                         center=False, window = 100).std()
        temp['15wkRollingStdDev'] = temp['LogRet'].rolling(
                                         center=False, window = 75).std()
        temp['12wkRollingStdDev'] = temp['LogRet'].rolling(
                                         center=False, window = 60).std()
        temp['11wkRollingStdDev'] = temp['LogRet'].rolling(
                                         center=False, window = 55).std()
        temp['10wkRollingStdDev'] = temp['LogRet'].rolling(
                                         center=False, window = 50).std()
        temp['9wkRollingStdDev'] = temp['LogRet'].rolling(
                                         center=False, window = 45).std()
        temp['8wkRollingStdDev'] = temp['LogRet'].rolling(
                                         center=False, window = 40).std()
        temp['7wkRollingStdDev'] = temp['LogRet'].rolling(
                                         center=False, window = 35).std()
        temp['6wkRollingStdDev'] = temp['LogRet'].rolling(
                                         center=False, window = 30).std()
        temp['5wkRollingStdDev'] = temp['LogRet'].rolling(
                                         center=False, window = 25).std()                                         
        temp['4wkRollingStdDev'] = temp['LogRet'].rolling(
                                         center=False, window = 20).std()
        temp['3wkRollingStdDev'] = temp['LogRet'].rolling(
                                         center=False, window = 15).std()
        temp['2wkRollingStdDev'] = temp['LogRet'].rolling(
                                         center=False, window = 10).std()
        temp['1wkRollingStdDev'] = temp['LogRet'].rolling(
                                         center=False, window = 5).std()
        temp['4dayRollingStdDev'] = temp['LogRet'].rolling(
                                         center=False, window = 4).std()
        temp['3dayRollingStdDev'] = temp['LogRet'].rolling(
                                         center=False, window = 3).std()
        temp['2dayRollingStdDev'] = temp['LogRet'].rolling(
                                         center=False, window = 2).std()
        #Rate of Change (ROC) in %
        temp['100wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(500)
                                          ) / temp['Adj Close'].shift(500)  
        temp['100wkRateOfChange'] = temp['100wkRateOfChange'].fillna(0)
        temp['90wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(450)
                                          ) / temp['Adj Close'].shift(450)  
        temp['90wkRateOfChange'] = temp['90wkRateOfChange'].fillna(0)
        temp['80wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(400)
                                          ) / temp['Adj Close'].shift(400)  
        temp['80wkRateOfChange'] = temp['80wkRateOfChange'].fillna(0)
        temp['70wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(350)
                                          ) / temp['Adj Close'].shift(350)  
        temp['70wkRateOfChange'] = temp['70wkRateOfChange'].fillna(0)
        temp['65wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(325)
                                          ) / temp['Adj Close'].shift(325)  
        temp['65wkRateOfChange'] = temp['65wkRateOfChange'].fillna(0)
        temp['60wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(300)
                                          ) / temp['Adj Close'].shift(300)  
        temp['60wkRateOfChange'] = temp['60wkRateOfChange'].fillna(0)
        temp['55wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(275)
                                          ) / temp['Adj Close'].shift(275)  
        temp['55wkRateOfChange'] = temp['55wkRateOfChange'].fillna(0)
        temp['52wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(252)
                                          ) / temp['Adj Close'].shift(252)  
        temp['52wkRateOfChange'] = temp['52wkRateOfChange'].fillna(0)
        temp['45wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(225)
                                          ) / temp['Adj Close'].shift(225)  
        temp['45wkRateOfChange'] = temp['45wkRateOfChange'].fillna(0)
        temp['40wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(200)
                                          ) / temp['Adj Close'].shift(200)  
        temp['40wkRateOfChange'] = temp['40wkRateOfChange'].fillna(0)
        temp['35wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(175)
                                          ) / temp['Adj Close'].shift(175)  
        temp['35wkRateOfChange'] = temp['35wkRateOfChange'].fillna(0)
        temp['30wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(150)
                                          ) / temp['Adj Close'].shift(150)  
        temp['30wkRateOfChange'] = temp['30wkRateOfChange'].fillna(0)
        temp['25wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(125)
                                          ) / temp['Adj Close'].shift(125)  
        temp['25wkRateOfChange'] = temp['25wkRateOfChange'].fillna(0)
        temp['20wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(100)
                                          ) / temp['Adj Close'].shift(100)  
        temp['20wkRateOfChange'] = temp['20wkRateOfChange'].fillna(0)
        temp['15wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(75)
                                          ) / temp['Adj Close'].shift(75)  
        temp['15wkRateOfChange'] = temp['15wkRateOfChange'].fillna(0)
        temp['12wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(60)
                                          ) / temp['Adj Close'].shift(60)  
        temp['12wkRateOfChange'] = temp['12wkRateOfChange'].fillna(0)
        temp['11wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(55)
                                          ) / temp['Adj Close'].shift(55)  
        temp['11wkRateOfChange'] = temp['11wkRateOfChange'].fillna(0)
        temp['10wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(50)
                                          ) / temp['Adj Close'].shift(50)  
        temp['10wkRateOfChange'] = temp['10wkRateOfChange'].fillna(0)
        temp['9wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(45)
                                          ) / temp['Adj Close'].shift(45)  
        temp['9wkRateOfChange'] = temp['9wkRateOfChange'].fillna(0)
        temp['8wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(40)
                                          ) / temp['Adj Close'].shift(40)  
        temp['8wkRateOfChange'] = temp['8wkRateOfChange'].fillna(0)
        temp['7wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(35)
                                          ) / temp['Adj Close'].shift(35)  
        temp['7wkRateOfChange'] = temp['7wkRateOfChange'].fillna(0)
        temp['6wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(30)
                                          ) / temp['Adj Close'].shift(30)  
        temp['6wkRateOfChange'] = temp['6wkRateOfChange'].fillna(0)
        temp['5wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(25)
                                          ) / temp['Adj Close'].shift(25)  
        temp['5wkRateOfChange'] = temp['5wkRateOfChange'].fillna(0)
        temp['4wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(20)
                                          ) / temp['Adj Close'].shift(20)  
        temp['4wkRateOfChange'] = temp['4wkRateOfChange'].fillna(0)
        temp['3wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(15)
                                          ) / temp['Adj Close'].shift(15)  
        temp['3wkRateOfChange'] = temp['3wkRateOfChange'].fillna(0)
        temp['2wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(10)
                                          ) / temp['Adj Close'].shift(10)  
        temp['2wkRateOfChange'] = temp['2wkRateOfChange'].fillna(0)        
        temp['1wkRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(5)
                                          ) / temp['Adj Close'].shift(5)  
        temp['1wkRateOfChange'] = temp['1wkRateOfChange'].fillna(0)
        temp['4dayRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(4)
                                          ) / temp['Adj Close'].shift(4)  
        temp['4dayRateOfChange'] = temp['4dayRateOfChange'].fillna(0)
        temp['3dayRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(3)
                                          ) / temp['Adj Close'].shift(3)  
        temp['3dayRateOfChange'] = temp['3dayRateOfChange'].fillna(0)        
        temp['2dayRateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(2)
                                          ) / temp['Adj Close'].shift(2)  
        temp['2dayRateOfChange'] = temp['2dayRateOfChange'].fillna(0)

        #Over rolling period Average volume in period
        temp['100wkRollingAverageVolume'] = temp['Volume'].rolling(
                                           center=False, window=500).mean()
        temp['90wkRollingAverageVolume'] = temp['Volume'].rolling(
                                           center=False, window=450).mean()
        temp['80wkRollingAverageVolume'] = temp['Volume'].rolling(
                                           center=False, window=400).mean()
        temp['70wkRollingAverageVolume'] = temp['Volume'].rolling(
                                           center=False, window=350).mean()
        temp['65wkRollingAverageVolume'] = temp['Volume'].rolling(
                                           center=False, window=325).mean()
        temp['60wkRollingAverageVolume'] = temp['Volume'].rolling(
                                           center=False, window=300).mean()
        temp['55wkRollingAverageVolume'] = temp['Volume'].rolling(
                                           center=False, window=275).mean()
        temp['52wkRollingAverageVolume'] = temp['Volume'].rolling(
                                           center=False, window=252).mean()
        temp['45wkRollingAverageVolume'] = temp['Volume'].rolling(
                                           center=False, window=225).mean()
        temp['40wkRollingAverageVolume'] = temp['Volume'].rolling(
                                           center=False, window=200).mean()
        temp['35wkRollingAverageVolume'] = temp['Volume'].rolling(
                                           center=False, window=175).mean()
        temp['30wkRollingAverageVolume'] = temp['Volume'].rolling(
                                           center=False, window=150).mean()
        temp['25wkRollingAverageVolume'] = temp['Volume'].rolling(
                                           center=False, window=125).mean()
        temp['20wkRollingAverageVolume'] = temp['Volume'].rolling(
                                           center=False, window=100).mean()
        temp['15wkRollingAverageVolume'] = temp['Volume'].rolling(
                                           center=False, window=75).mean()
        temp['12wkRollingAverageVolume'] = temp['Volume'].rolling(
                                           center=False, window=60).mean()
        temp['11wkRollingAverageVolume'] = temp['Volume'].rolling(
                                           center=False, window=55).mean()
        temp['10wkRollingAverageVolume'] = temp['Volume'].rolling(
                                           center=False, window=50).mean()
        temp['9wkRollingAverageVolume'] = temp['Volume'].rolling(
                                           center=False, window=45).mean()
        temp['8wkRollingAverageVolume'] = temp['Volume'].rolling(
                                           center=False, window=40).mean()
        temp['7wkRollingAverageVolume'] = temp['Volume'].rolling(
                                           center=False, window=35).mean()
        temp['6wkRollingAverageVolume'] = temp['Volume'].rolling(
                                           center=False, window=30).mean()
        temp['5wkRollingAverageVolume'] = temp['Volume'].rolling(
                                           center=False, window=25).mean()
        temp['4wkRollingAverageVolume'] = temp['Volume'].rolling(
                                           center=False, window=20).mean()
        temp['3wkRollingAverageVolume'] = temp['Volume'].rolling(
                                           center=False, window=15).mean()
        temp['2wkRollingAverageVolume'] = temp['Volume'].rolling(
                                           center=False, window=10).mean()
        temp['1wkRollingAverageVolume'] = temp['Volume'].rolling(
                                           center=False, window=5).mean()   
        temp['4dayRollingAverageVolume'] = temp['Volume'].rolling(
                                           center=False, window=4).mean()  
        temp['3dayRollingAverageVolume'] = temp['Volume'].rolling(
                                           center=False, window=3).mean()  
        temp['2dayRollingAverageVolume'] = temp['Volume'].rolling(
                                           center=False, window=2).mean()                                             
                                           
        #Front period over Average Return
        temp['100wkRollingReturnOverAverage'] = (temp['100wkRollingAverageReturn']/ 
                                                temp['100wkTotalAverageReturn'])
        temp['90wkRollingReturnOverAverage'] = (temp['90wkRollingAverageReturn']/ 
                                                temp['90wkTotalAverageReturn'])
        temp['80wkRollingReturnOverAverage'] = (temp['80wkRollingAverageReturn']/ 
                                                temp['80wkTotalAverageReturn'])
        temp['70wkRollingReturnOverAverage'] = (temp['70wkRollingAverageReturn']/ 
                                                temp['70wkTotalAverageReturn'])
        temp['65wkRollingReturnOverAverage'] = (temp['65wkRollingAverageReturn']/ 
                                                temp['65wkTotalAverageReturn'])
        temp['60wkRollingReturnOverAverage'] = (temp['60wkRollingAverageReturn']/ 
                                                temp['60wkTotalAverageReturn'])
        temp['55wkRollingReturnOverAverage'] = (temp['55wkRollingAverageReturn']/ 
                                                temp['55wkTotalAverageReturn'])
        temp['52wkRollingReturnOverAverage'] = (temp['52wkRollingAverageReturn']/ 
                                                temp['52wkTotalAverageReturn'])
        temp['45wkRollingReturnOverAverage'] = (temp['45wkRollingAverageReturn']/ 
                                                temp['45wkTotalAverageReturn'])
        temp['40wkRollingReturnOverAverage'] = (temp['40wkRollingAverageReturn']/ 
                                                temp['40wkTotalAverageReturn'])
        temp['35wkRollingReturnOverAverage'] = (temp['35wkRollingAverageReturn']/ 
                                                temp['35wkTotalAverageReturn'])
        temp['30wkRollingReturnOverAverage'] = (temp['30wkRollingAverageReturn']/ 
                                                temp['30wkTotalAverageReturn'])
        temp['25wkRollingReturnOverAverage'] = (temp['25wkRollingAverageReturn']/ 
                                                temp['25wkTotalAverageReturn'])
        temp['20wkRollingReturnOverAverage'] = (temp['20wkRollingAverageReturn']/ 
                                                temp['20wkTotalAverageReturn'])
        temp['15wkRollingReturnOverAverage'] = (temp['15wkRollingAverageReturn']/ 
                                                temp['15wkTotalAverageReturn'])
        temp['12wkRollingReturnOverAverage'] = (temp['12wkRollingAverageReturn']/ 
                                                temp['12wkTotalAverageReturn'])
        temp['11wkRollingReturnOverAverage'] = (temp['11wkRollingAverageReturn']/ 
                                                temp['11wkTotalAverageReturn'])
        temp['10wkRollingReturnOverAverage'] = (temp['10wkRollingAverageReturn']/ 
                                                temp['10wkTotalAverageReturn'])
        temp['9wkRollingReturnOverAverage'] =  (temp['9wkRollingAverageReturn']/ 
                                                temp['9wkTotalAverageReturn'])
        temp['8wkRollingReturnOverAverage'] =  (temp['8wkRollingAverageReturn']/ 
                                                temp['8wkTotalAverageReturn'])
        temp['7wkRollingReturnOverAverage'] =  (temp['7wkRollingAverageReturn']/ 
                                                temp['7wkTotalAverageReturn'])
        temp['6wkRollingReturnOverAverage'] =  (temp['6wkRollingAverageReturn']/ 
                                                temp['6wkTotalAverageReturn'])
        temp['5wkRollingReturnOverAverage'] =  (temp['5wkRollingAverageReturn']/ 
                                                temp['5wkTotalAverageReturn'])
        temp['4wkRollingReturnOverAverage'] =  (temp['4wkRollingAverageReturn']/ 
                                                temp['4wkTotalAverageReturn'])
        temp['3wkRollingReturnOverAverage'] =  (temp['3wkRollingAverageReturn']/ 
                                                temp['3wkTotalAverageReturn'])
        temp['2wkRollingReturnOverAverage'] =  (temp['2wkRollingAverageReturn']/ 
                                                temp['2wkTotalAverageReturn'])
        temp['1wkRollingReturnOverAverage'] =  (temp['1wkRollingAverageReturn']/ 
                                                temp['1wkTotalAverageReturn'])
        temp['4dayRollingReturnOverAverage'] = (temp['4dayRollingAverageReturn']/ 
                                                temp['4dayTotalAverageReturn'])
        temp['3dayRollingReturnOverAverage'] = (temp['3dayRollingAverageReturn']/ 
                                                temp['3dayTotalAverageReturn'])
        temp['2dayRollingReturnOverAverage'] = (temp['2dayRollingAverageReturn']/ 
                                                temp['2dayTotalAverageReturn'])                                                

        #Front period over Average Std Dev      // These are ratios                                
        temp['100wkRollingStdDevOverAverage'] = (temp['52wkRollingStdDev']/ 
                                                temp['52wkTotalAverageStdDev'])
        temp['90wkRollingStdDevOverAverage'] = (temp['52wkRollingStdDev']/ 
                                                temp['52wkTotalAverageStdDev'])
        temp['80wkRollingStdDevOverAverage'] = (temp['52wkRollingStdDev']/ 
                                                temp['52wkTotalAverageStdDev'])
        temp['70wkRollingStdDevOverAverage'] = (temp['52wkRollingStdDev']/ 
                                                temp['52wkTotalAverageStdDev'])
        temp['65wkRollingStdDevOverAverage'] = (temp['52wkRollingStdDev']/ 
                                                temp['52wkTotalAverageStdDev'])
        temp['60wkRollingStdDevOverAverage'] = (temp['52wkRollingStdDev']/ 
                                                temp['52wkTotalAverageStdDev'])
        temp['55wkRollingStdDevOverAverage'] = (temp['52wkRollingStdDev']/ 
                                                temp['52wkTotalAverageStdDev'])
        temp['52wkRollingStdDevOverAverage'] = (temp['52wkRollingStdDev']/ 
                                                temp['52wkTotalAverageStdDev'])
        temp['45wkRollingStdDevOverAverage'] = (temp['52wkRollingStdDev']/ 
                                                temp['52wkTotalAverageStdDev'])
        temp['40wkRollingStdDevOverAverage'] = (temp['52wkRollingStdDev']/ 
                                                temp['52wkTotalAverageStdDev'])
        temp['35wkRollingStdDevOverAverage'] = (temp['52wkRollingStdDev']/ 
                                                temp['52wkTotalAverageStdDev'])
        temp['30wkRollingStdDevOverAverage'] = (temp['52wkRollingStdDev']/ 
                                                temp['52wkTotalAverageStdDev'])
        temp['25wkRollingStdDevOverAverage'] = (temp['52wkRollingStdDev']/ 
                                                temp['52wkTotalAverageStdDev'])
        temp['20wkRollingStdDevOverAverage'] = (temp['52wkRollingStdDev']/ 
                                                temp['52wkTotalAverageStdDev'])
        temp['15wkRollingStdDevOverAverage'] = (temp['52wkRollingStdDev']/ 
                                                temp['52wkTotalAverageStdDev'])
        temp['12wkRollingStdDevOverAverage'] = (temp['52wkRollingStdDev']/ 
                                                temp['52wkTotalAverageStdDev'])
        temp['11wkRollingStdDevOverAverage'] = (temp['52wkRollingStdDev']/ 
                                                temp['52wkTotalAverageStdDev'])
        temp['10wkRollingStdDevOverAverage'] = (temp['52wkRollingStdDev']/ 
                                                temp['52wkTotalAverageStdDev'])
        temp['9wkRollingStdDevOverAverage'] = (temp['52wkRollingStdDev']/ 
                                                temp['52wkTotalAverageStdDev'])
        temp['8wkRollingStdDevOverAverage'] = (temp['52wkRollingStdDev']/ 
                                                temp['52wkTotalAverageStdDev'])
        temp['7wkRollingStdDevOverAverage'] = (temp['52wkRollingStdDev']/ 
                                                temp['52wkTotalAverageStdDev'])
        temp['6wkRollingStdDevOverAverage'] = (temp['52wkRollingStdDev']/ 
                                                temp['52wkTotalAverageStdDev'])
        temp['5wkRollingStdDevOverAverage'] = (temp['52wkRollingStdDev']/ 
                                                temp['52wkTotalAverageStdDev'])
        temp['4wkRollingStdDevOverAverage'] = (temp['52wkRollingStdDev']/ 
                                                temp['52wkTotalAverageStdDev'])
        temp['3wkRollingStdDevOverAverage'] = (temp['52wkRollingStdDev']/ 
                                                temp['52wkTotalAverageStdDev'])
        temp['2wkRollingStdDevOverAverage'] = (temp['52wkRollingStdDev']/ 
                                                temp['52wkTotalAverageStdDev'])
        temp['1wkRollingStdDevOverAverage'] = (temp['52wkRollingStdDev']/ 
                                                temp['52wkTotalAverageStdDev'])
        temp['4dayRollingStdDevOverAverage'] = (temp['52wkRollingStdDev']/ 
                                                temp['52wkTotalAverageStdDev'])
        temp['3dayRollingStdDevOverAverage'] = (temp['52wkRollingStdDev']/ 
                                                temp['52wkTotalAverageStdDev'])
        temp['2dayRollingStdDevOverAverage'] = (temp['52wkRollingStdDev']/ 
                                                temp['52wkTotalAverageStdDev'])                        

        #Gap Up
        temp['GapUp'] = (temp['High'].shift(1) - temp['Low']) / temp['Adj Close'].shift(1)
        temp['GapUp'] = temp['GapUp'][temp['GapUp'] < 0]
        temp['GapUp'] = temp['GapUp'].fillna(0)
        temp['GapUp'] = np.where(temp['GapUp'] == 0 , 0, (-1*temp['GapUp']))

        #Gap Down
        temp['GapDown'] = (temp['Low'].shift(1) - temp['High']) / temp['Adj Close'].shift(1)
        temp['GapDown'] = temp['GapDown'][temp['GapDown'] > 0]
        temp['GapDown'] = temp['GapDown'].fillna(0)
        
        #ATR Setup
        temp['Method1'] = temp['High'] - temp['Low']
        temp['Method2'] = abs((temp['High'] - temp['Adj Close'].shift(1)))
        temp['Method3'] = abs((temp['Low'] - temp['Adj Close'].shift(1)))
        temp['Method1'] = temp['Method1'].fillna(0)
        temp['Method2'] = temp['Method2'].fillna(0)
        temp['Method3'] = temp['Method3'].fillna(0)
        temp['TrueRange'] = temp[['Method1','Method2','Method3']].max(axis = 1)

        #ATR Calculation
        temp['100wkATRPoints'] = temp['TrueRange'].rolling(window = 500, center=False).mean()        
        temp['100wkATRPercent'] = temp['100wkATRPoints'] / temp['Adj Close']
        temp['90wkATRPoints'] = temp['TrueRange'].rolling(window = 450, center=False).mean()        
        temp['90wkATRPercent'] = temp['90wkATRPoints'] / temp['Adj Close']
        temp['80wkATRPoints'] = temp['TrueRange'].rolling(window = 400, center=False).mean()        
        temp['80wkATRPercent'] = temp['80wkATRPoints'] / temp['Adj Close']
        temp['70wkATRPoints'] = temp['TrueRange'].rolling(window = 350, center=False).mean()        
        temp['70wkATRPercent'] = temp['70wkATRPoints'] / temp['Adj Close']
        temp['65wkATRPoints'] = temp['TrueRange'].rolling(window = 325, center=False).mean()        
        temp['65wkATRPercent'] = temp['65wkATRPoints'] / temp['Adj Close']
        temp['60wkATRPoints'] = temp['TrueRange'].rolling(window = 300, center=False).mean()        
        temp['60wkATRPercent'] = temp['60wkATRPoints'] / temp['Adj Close']
        temp['55wkATRPoints'] = temp['TrueRange'].rolling(window = 275, center=False).mean()        
        temp['55wkATRPercent'] = temp['55wkATRPoints'] / temp['Adj Close']
        temp['52wkATRPoints'] = temp['TrueRange'].rolling(window = 252, center=False).mean()        
        temp['52wkATRPercent'] = temp['52wkATRPoints'] / temp['Adj Close']
        temp['45wkATRPoints'] = temp['TrueRange'].rolling(window = 225, center=False).mean()        
        temp['45wkATRPercent'] = temp['45wkATRPoints'] / temp['Adj Close']
        temp['40wkATRPoints'] = temp['TrueRange'].rolling(window = 200, center=False).mean()        
        temp['40wkATRPercent'] = temp['40wkATRPoints'] / temp['Adj Close']
        temp['35wkATRPoints'] = temp['TrueRange'].rolling(window = 175, center=False).mean()        
        temp['35wkATRPercent'] = temp['35wkATRPoints'] / temp['Adj Close']
        temp['30wkATRPoints'] = temp['TrueRange'].rolling(window = 150, center=False).mean()        
        temp['30wkATRPercent'] = temp['30wkATRPoints'] / temp['Adj Close']
        temp['25wkATRPoints'] = temp['TrueRange'].rolling(window = 125, center=False).mean()        
        temp['25wkATRPercent'] = temp['25wkATRPoints'] / temp['Adj Close']
        temp['20wkATRPoints'] = temp['TrueRange'].rolling(window = 100, center=False).mean()        
        temp['20wkATRPercent'] = temp['20wkATRPoints'] / temp['Adj Close']
        temp['15wkATRPoints'] = temp['TrueRange'].rolling(window = 75, center=False).mean()        
        temp['15wkATRPercent'] = temp['15wkATRPoints'] / temp['Adj Close']
        temp['12wkATRPoints'] = temp['TrueRange'].rolling(window = 60, center=False).mean()        
        temp['12wkATRPercent'] = temp['12wkATRPoints'] / temp['Adj Close']
        temp['11wkATRPoints'] = temp['TrueRange'].rolling(window = 55, center=False).mean()        
        temp['11wkATRPercent'] = temp['11wkATRPoints'] / temp['Adj Close']
        temp['10wkATRPoints'] = temp['TrueRange'].rolling(window = 50, center=False).mean()        
        temp['10wkATRPercent'] = temp['10wkATRPoints'] / temp['Adj Close']
        temp['9wkATRPoints'] = temp['TrueRange'].rolling(window = 45, center=False).mean()        
        temp['9wkATRPercent'] = temp['9wkATRPoints'] / temp['Adj Close']
        temp['8wkATRPoints'] = temp['TrueRange'].rolling(window = 40, center=False).mean()        
        temp['8wkATRPercent'] = temp['8wkATRPoints'] / temp['Adj Close']
        temp['7wkATRPoints'] = temp['TrueRange'].rolling(window = 35, center=False).mean()        
        temp['7wkATRPercent'] = temp['7wkATRPoints'] / temp['Adj Close']
        temp['6wkATRPoints'] = temp['TrueRange'].rolling(window = 30, center=False).mean()        
        temp['6wkATRPercent'] = temp['6wkATRPoints'] / temp['Adj Close']
        temp['5wkATRPoints'] = temp['TrueRange'].rolling(window = 25, center=False).mean()        
        temp['5wkATRPercent'] = temp['5wkATRPoints'] / temp['Adj Close']
        temp['4wkATRPoints'] = temp['TrueRange'].rolling(window = 20, center=False).mean()        
        temp['4wkATRPercent'] = temp['4wkATRPoints'] / temp['Adj Close']
        temp['3wkATRPoints'] = temp['TrueRange'].rolling(window = 15, center=False).mean()        
        temp['3wkATRPercent'] = temp['3wkATRPoints'] / temp['Adj Close']
        temp['2wkATRPoints'] = temp['TrueRange'].rolling(window = 10, center=False).mean()        
        temp['2wkATRPercent'] = temp['2wkATRPoints'] / temp['Adj Close']
        temp['1wkATRPoints'] = temp['TrueRange'].rolling(window = 5, center=False).mean()        
        temp['1wkATRPercent'] = temp['1wkATRPoints'] / temp['Adj Close']
        temp['4dayATRPoints'] = temp['TrueRange'].rolling(window = 4, center=False).mean()        
        temp['4dayATRPercent'] = temp['4dayATRPoints'] / temp['Adj Close']
        temp['3dayATRPoints'] = temp['TrueRange'].rolling(window = 3, center=False).mean()        
        temp['3dayATRPercent'] = temp['3dayATRPoints'] / temp['Adj Close']
        temp['2dayATRPoints'] = temp['TrueRange'].rolling(window = 2, center=False).mean()        
        temp['2dayATRPercent'] = temp['2dayATRPoints'] / temp['Adj Close']        
       
        #Efficiency (is normalized across markets by Diff/ATR)                                          
        temp['100wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(500)
        temp['100wkEfficiency'] = temp['100wkCloseDiff'] / temp['100wkATRPoints'] 
        temp['90wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(450)
        temp['90wkEfficiency'] = temp['90wkCloseDiff'] / temp['90wkATRPoints'] 
        temp['80wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(400)
        temp['80wkEfficiency'] = temp['80wkCloseDiff'] / temp['80wkATRPoints'] 
        temp['70wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(350)
        temp['70wkEfficiency'] = temp['70wkCloseDiff'] / temp['70wkATRPoints'] 
        temp['65wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(325)
        temp['65wkEfficiency'] = temp['65wkCloseDiff'] / temp['65wkATRPoints'] 
        temp['60wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(300)
        temp['60wkEfficiency'] = temp['60wkCloseDiff'] / temp['60wkATRPoints'] 
        temp['55wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(275)
        temp['55wkEfficiency'] = temp['55wkCloseDiff'] / temp['55wkATRPoints'] 
        temp['52wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(252)
        temp['52wkEfficiency'] = temp['52wkCloseDiff'] / temp['52wkATRPoints'] 
        temp['45wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(225)
        temp['45wkEfficiency'] = temp['45wkCloseDiff'] / temp['45wkATRPoints'] 
        temp['40wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(200)
        temp['40wkEfficiency'] = temp['40wkCloseDiff'] / temp['40wkATRPoints'] 
        temp['35wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(175)
        temp['35wkEfficiency'] = temp['35wkCloseDiff'] / temp['35wkATRPoints'] 
        temp['30wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(150)
        temp['30wkEfficiency'] = temp['30wkCloseDiff'] / temp['30wkATRPoints'] 
        temp['25wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(125)
        temp['25wkEfficiency'] = temp['25wkCloseDiff'] / temp['25wkATRPoints'] 
        temp['20wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(100)
        temp['20wkEfficiency'] = temp['20wkCloseDiff'] / temp['20wkATRPoints'] 
        temp['15wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(75)
        temp['15wkEfficiency'] = temp['15wkCloseDiff'] / temp['15wkATRPoints'] 
        temp['12wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(60)
        temp['12wkEfficiency'] = temp['12wkCloseDiff'] / temp['12wkATRPoints'] 
        temp['11wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(55)
        temp['11wkEfficiency'] = temp['11wkCloseDiff'] / temp['11wkATRPoints'] 
        temp['10wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(50)
        temp['10wkEfficiency'] = temp['10wkCloseDiff'] / temp['10wkATRPoints'] 
        temp['9wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(45)
        temp['9wkEfficiency'] = temp['9wkCloseDiff'] / temp['9wkATRPoints'] 
        temp['8wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(40)
        temp['8wkEfficiency'] = temp['8wkCloseDiff'] / temp['8wkATRPoints'] 
        temp['7wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(35)
        temp['7wkEfficiency'] = temp['7wkCloseDiff'] / temp['7wkATRPoints'] 
        temp['6wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(30)
        temp['6wkEfficiency'] = temp['6wkCloseDiff'] / temp['6wkATRPoints'] 
        temp['5wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(25)
        temp['5wkEfficiency'] = temp['5wkCloseDiff'] / temp['5wkATRPoints'] 
        temp['4wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(20)
        temp['4wkEfficiency'] = temp['4wkCloseDiff'] / temp['4wkATRPoints'] 
        temp['3wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(15)
        temp['3wkEfficiency'] = temp['3wkCloseDiff'] / temp['3wkATRPoints'] 
        temp['2wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(10)
        temp['2wkEfficiency'] = temp['2wkCloseDiff'] / temp['2wkATRPoints'] 
        temp['1wkCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(5)
        temp['1wkEfficiency'] = temp['1wkCloseDiff'] / temp['1wkATRPoints'] 
        temp['4dayCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(4)
        temp['4dayEfficiency'] = temp['4dayCloseDiff'] / temp['4dayATRPoints'] 
        temp['3dayCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(3)
        temp['3dayEfficiency'] = temp['3dayCloseDiff'] / temp['3dayATRPoints'] 
        temp['2dayCloseDiff'] = temp['Adj Close'] - temp['Adj Close'].shift(2)
        temp['2dayEfficiency'] = temp['2dayCloseDiff'] / temp['2dayATRPoints'] 
      
        #average rolling volume
        temp['100wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                            window=500).mean() 
        temp['90wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                            window=450).mean() 
        temp['80wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                            window=400).mean() 
        temp['70wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                            window=350).mean() 
        temp['65wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                            window=325).mean()                                                             
        temp['60wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                            window=300).mean() 
        temp['55wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                            window=275).mean() 
        temp['52wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                            window=252).mean() 
        temp['45wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                            window=225).mean() 
        temp['40wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                            window=200).mean() 
        temp['35wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                            window=175).mean() 
        temp['30wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                            window=150).mean() 
        temp['25wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                            window=125).mean()  
        temp['20wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                            window=100).mean() 
        temp['15wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                            window=75).mean() 
        temp['12wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                            window=60).mean() 
        temp['11wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                            window=55).mean()                                                             
        temp['10wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                            window=50).mean() 
        temp['9wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                            window=45).mean() 
        temp['8wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                            window=40).mean() 
        temp['7wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                            window=35).mean() 
        temp['6wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                            window=30).mean() 
        temp['5wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                            window=25).mean() 
        temp['4wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                            window=20).mean() 
        temp['3wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                            window=15).mean() 
        temp['2wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                            window=10).mean() 
        temp['1wkAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                            window=5).mean() 
        temp['4dayAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                            window=4).mean() 
        temp['3dayAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                            window=3).mean() 
        temp['2dayAverageRollingVolume'] = temp['Volume'].rolling(center=False, 
                                                            window=2).mean()
                                                             
        #Make also a float estimation
        temp['Float'] = 0
        
        #Simple Moving Average
        temp['100wkSMA'] = temp['Adj Close'].rolling(window=500, center=False).mean()
        temp['100wkSMA'] = temp['100wkSMA'].fillna(0)
        temp['90wkSMA'] = temp['Adj Close'].rolling(window=450, center=False).mean()
        temp['90wkSMA'] = temp['90wkSMA'].fillna(0)
        temp['80wkSMA'] = temp['Adj Close'].rolling(window=400, center=False).mean()
        temp['80wkSMA'] = temp['80wkSMA'].fillna(0)
        temp['70wkSMA'] = temp['Adj Close'].rolling(window=350, center=False).mean()
        temp['70wkSMA'] = temp['70wkSMA'].fillna(0)
        temp['65wkSMA'] = temp['Adj Close'].rolling(window=325, center=False).mean()
        temp['65wkSMA'] = temp['65wkSMA'].fillna(0)
        temp['60wkSMA'] = temp['Adj Close'].rolling(window=300, center=False).mean()
        temp['60wkSMA'] = temp['60wkSMA'].fillna(0)
        temp['55wkSMA'] = temp['Adj Close'].rolling(window=275, center=False).mean()
        temp['55wkSMA'] = temp['55wkSMA'].fillna(0)
        temp['52wkSMA'] = temp['Adj Close'].rolling(window=252, center=False).mean()
        temp['52wkSMA'] = temp['52wkSMA'].fillna(0)
        temp['45wkSMA'] = temp['Adj Close'].rolling(window=225, center=False).mean()
        temp['45wkSMA'] = temp['45wkSMA'].fillna(0)
        temp['40wkSMA'] = temp['Adj Close'].rolling(window=200, center=False).mean()
        temp['40wkSMA'] = temp['40wkSMA'].fillna(0)
        temp['35wkSMA'] = temp['Adj Close'].rolling(window=175, center=False).mean()
        temp['35wkSMA'] = temp['35wkSMA'].fillna(0)
        temp['30wkSMA'] = temp['Adj Close'].rolling(window=150, center=False).mean()
        temp['30wkSMA'] = temp['30wkSMA'].fillna(0)
        temp['25wkSMA'] = temp['Adj Close'].rolling(window=125, center=False).mean()
        temp['25wkSMA'] = temp['25wkSMA'].fillna(0)
        temp['20wkSMA'] = temp['Adj Close'].rolling(window=100, center=False).mean()
        temp['20wkSMA'] = temp['20wkSMA'].fillna(0)
        temp['15wkSMA'] = temp['Adj Close'].rolling(window=75, center=False).mean()
        temp['15wkSMA'] = temp['15wkSMA'].fillna(0)
        temp['12wkSMA'] = temp['Adj Close'].rolling(window=60, center=False).mean()
        temp['12wkSMA'] = temp['12wkSMA'].fillna(0)
        temp['11wkSMA'] = temp['Adj Close'].rolling(window=55, center=False).mean()
        temp['11wkSMA'] = temp['11wkSMA'].fillna(0)
        temp['10wkSMA'] = temp['Adj Close'].rolling(window=50, center=False).mean()
        temp['10wkSMA'] = temp['10wkSMA'].fillna(0)
        temp['9wkSMA'] = temp['Adj Close'].rolling(window=45, center=False).mean()
        temp['9wkSMA'] = temp['9wkSMA'].fillna(0)
        temp['8wkSMA'] = temp['Adj Close'].rolling(window=40, center=False).mean()
        temp['8wkSMA'] = temp['8wkSMA'].fillna(0)
        temp['7wkSMA'] = temp['Adj Close'].rolling(window=35, center=False).mean()
        temp['7wkSMA'] = temp['7wkSMA'].fillna(0)
        temp['6wkSMA'] = temp['Adj Close'].rolling(window=30, center=False).mean()
        temp['6wkSMA'] = temp['6wkSMA'].fillna(0)
        temp['5wkSMA'] = temp['Adj Close'].rolling(window=25, center=False).mean()
        temp['5wkSMA'] = temp['5wkSMA'].fillna(0)
        temp['4wkSMA'] = temp['Adj Close'].rolling(window=20, center=False).mean()
        temp['4wkSMA'] = temp['4wkSMA'].fillna(0)
        temp['3wkSMA'] = temp['Adj Close'].rolling(window=15, center=False).mean()
        temp['3wkSMA'] = temp['3wkSMA'].fillna(0)
        temp['2wkSMA'] = temp['Adj Close'].rolling(window=10, center=False).mean()
        temp['2wkSMA'] = temp['2wkSMA'].fillna(0)
        temp['1wkSMA'] = temp['Adj Close'].rolling(window=5, center=False).mean()
        temp['1wkSMA'] = temp['1wkSMA'].fillna(0)
        temp['4daySMA'] = temp['Adj Close'].rolling(window=4, center=False).mean()
        temp['4daySMA'] = temp['4daySMA'].fillna(0)
        temp['3daySMA'] = temp['Adj Close'].rolling(window=3, center=False).mean()
        temp['3daySMA'] = temp['3daySMA'].fillna(0)
        temp['2daySMA'] = temp['Adj Close'].rolling(window=2, center=False).mean()
        temp['2daySMA'] = temp['2daySMA'].fillna(0)     
            
        #Market Range Analysis
        #ATR/Range             
            
#        #Drop Column Function
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