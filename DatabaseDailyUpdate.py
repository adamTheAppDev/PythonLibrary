# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a shortened version of a database update tool

#Import modules
import pandas as pd
import time as t
import webbrowser as web
from pandas import read_csv
from datetime import date
import datetime
import os
from io import StringIO
from pandas.parser import CParserError
import numpy as np
import requests

#Start timer
start1 = t.time()

#Variable assingment
idle = 0
today = date.today()

#To limit end date of time series
cutoffdatetime = datetime.date(2017, 6, 20) #should be June 20, 2017.
cutoffseconds = 1497949000
longtimeago = 1200000000
dayseconds = 86400
daysaway = int((today - cutoffdatetime).total_seconds()/dayseconds)
day = str(cutoffseconds + (daysaway * dayseconds))

#Use CrumbCatcher.py
artificialcrumb = "1.ZWRp1I9ZS" #Use crumbcatcher.py

#Universe list assignment
df = read_csv('C:\\Users\\UserName\\DirectoryLocation\\goodsymbols.csv', sep = ',')
symbol = df.Symbol.values
#For iteration tracking
ranger = range(0,len(df))

#URL assingment
firsthalf = "https://query1.finance.yahoo.com/v7/finance/download/" #insert ticker and add secondhalf
secondhalf = ("?period1=" + str(int(day) - dayseconds)  + "&period2=" + day +
           "&interval=1d&events=history&crumb=" + artificialcrumb) #1950 - most recent
secondhalf1 = ("?period1=" + str(longtimeago)  + "&period2=" + day +
"&interval=1d&events=history&crumb=" + artificialcrumb) #1950 - most recent

#URLs in DataFrame column
df['URL'] = firsthalf + df['Symbol'] + secondhalf

#For all tickers in directory
for i in ranger:
    try: 
        #Ticker name assignment
        ticker = str(df.Symbol[i])
        #Download URL assignment
        downloadurl = df['URL'][i]
#        mainurl = ("https://finance.yahoo.com/quote/" + ticker + "/history?p=" + ticker)
        #Making POST request
        response = requests.post(downloadurl)#, data=CookieDict)
        #Formatting
        datastr = response.text
        formatter = StringIO(datastr)
        strdf = pd.read_csv(formatter, sep = ',')
        #Check for invalid URL
        if strdf.columns[0] == '{"chart":{"result":null':
            print('The URL failed for ' + ticker)
            continue
        #More formatting
        strdf = strdf.set_index('Date')
        strdf.index = pd.to_datetime(strdf.index, format = "%Y/%m/%d") 
        #Save DataFrame to CSV
        strdf.to_csv(("F:\\Users\\UserName\\DirectoryLocation\\"+ ticker + ".csv"))
        #Confirming at end of loop
        print(ticker)
    except CParserError:
        print('Parser failed for ' + ticker)
        continue    

#List of items in directory
location = 'F:\\Users\\UserName\\DirectoryLocation'
midlist = os.listdir(location)

#If there's tables in directory
if len(midlist) > 0:
    #split string to get ticker names
    endlist = [x[:-4] for x in midlist]
    startlist = list(df['Symbol'])
    #tickers that need to be added that weren't added on first parse
    Needed = [x for x in startlist if x not in endlist]
    needf = pd.DataFrame(Needed, columns=['Symbol'])
    #Iterable for tickers needed   
    ranger1 = range(0,len(needf))
           
    #For all tickers that failed first parse, try again
    for j in ranger1:
        try:
            ticker = df['Symbol'][j]
            downloadurl = df['URL'][j]
#            mainurl = "https://finance.yahoo.com/quote/" + ticker + "/history?p=" + ticker
            response = requests.post(downloadurl)#, data=CookieDict)
            datastr = response.text
            formatter = StringIO(datastr)
            strdf = pd.read_csv(formatter, sep = ',')
            if strdf.columns[0] == '{"chart":{"result":null':
                print('The URL failed for ' + ticker)                
                continue
            strdf = strdf.set_index('Date')
            strdf.index = pd.to_datetime(strdf.index, format = "%Y/%m/%d") 
            strdf.to_csv(("F:\\Users\\UserName\\DirectoryLocation\\"+ ticker + ".csv"))
        except CParserError:
            print("The parser failed for" + ticker)
            continue
           
#List missing tickers from original parse
newmidlist = os.listdir(location)
newendlist = [x[:-4] for x in newmidlist]
newNeeded = [x for x in startlist if x not in newendlist]
print(str(len(newNeeded)) + ' Unimported Stocks Exist')
print("Missing symbols are --- > " + str(newNeeded))

#List all tickers in directory location
CSVlist = os.listdir("F:\\Users\\UserName\\DirectoryLocation\\")
#Iterable assignment
ranger = range(0,len(CSVlist))
ranger2 = range(0,len(os.listdir('F:\\Users\\UserName\\DirectoryLocation\\')))

#If there is files in Directory
if len(os.listdir('F:\\Users\\UserName\\DirectoryLocation\\')) > 1:
    #For each file
    for i in ranger:
        try:
            #Read file and store in temp varialbe
            temp = read_csv('F:\\Users\\UserName\\DirectoryLocation\\' +
            (CSVlist[i]), sep = ',')
            #Assign index to Date
            temp = temp.set_index('Date') 
            #Format
            temp.index = pd.to_datetime(temp.index, format = "%Y/%m/%d")
            #Save to pickle
            pd.to_pickle(temp, 'F:\\Users\\UserName\\DirectoryLocation\\' + 
                  CSVlist[i][:-4] + 'addition')
            #Read pickle
            glaze = pd.read_pickle('F:\\Users\\UserName\\DirectoryLocation\\' +
                         (CSVlist[i][:-4] + 'addition'))
            #For all columns in pickle
            for x in file.columns:
                #Make columns numeric type
                file[x] =  pd.to_numeric(file[x], errors='coerce')
            #Save file to pickle
            pd.to_pickle(file, 'F:\\Users\\UserName\\DirectoryLocation\\' +
                          CSVlist[i][:-4] + 'addition')      
            #Concatenating two separate files -- this is likely redundant
            bigpickle = pd.read_pickle('F:\\Users\\UserName\\DirectoryLocation\\' + 
                  CSVlist[i][:-4] + '\\' + CSVlist[i][:-4])
            littlepickle = pd.read_pickle('F:\\Users\\UserName\\DirectoryLocation\\' + 
                  CSVlist[i][:-4] + 'addition')
            newdata = pd.concat([bigpickle, littlepickle])
            #Save file to pickle
            pd.to_pickle(newdata, 'F:\\Users\\UserName\\DirectoryLocation\\' +
                          CSVlist[i][:-4] + '\\' + CSVlist[i][:-4])
        except OSError:
            continue                   
#Location variable assingment
tempPickle = 'F:\\Users\\UserName\\DirectoryLocation\\'
fileList2 = os.listdir(tempPickle)

#Removing all files from temp CSV folder -- clean up
for ff in fileList2:
    os.remove(tempPickle + "\\" + ff)

#Start timer for statistical data calculations
start = t.time()

#For all files in directory location
for ii in ranger2:
    try:
        #Read pickle to variable
        temp = pd.read_pickle('F:\\Users\\UserName\\DirectoryLocation\\' +
                CSVlist[ii][:-4]+ '\\' + CSVlist[ii][:-4])
        #For all columns
        for x in temp.columns:
            #Make tonumeric data type          
            temp[x] =  pd.to_numeric(temp[x], errors='coerce')
            #Then run all statistic and technical analysis
#                
#
#            temp['LogRet'] = np.log(temp['Adj Close']/temp['Adj Close'].shift(1)) 
#            temp['LogRet'] = temp['LogRet'].fillna(0)
#            
#            temp['52wkLow'] = temp['Adj Close'].rolling(252).min()
#            temp['52wkMax'] = temp['Adj Close'].rolling(252).max()
#            
#            temp['Age'] = len(temp['Open'])
#            
#            temp['TotalAverageAnnualReturn'] = temp['LogRet'].mean() * 252
#            
#            temp['TotalAverageAnnualStandardDeviation'] = temp['LogRet'].std(
#                                                                 )*np.sqrt(252)
#            
#            temp['CoefficientOfVaration'] = (
#            temp['TotalAverageAnnualStandardDeviation']/temp['TotalAverageAnnualReturn'])
#            
#            temp['Rolling52wkMockReturn'] = temp['LogRet'].rolling(
#                                             center=False, window = 252).mean()
#            
#            temp['Rolling52wkReturn'] = np.log(temp['Adj Close']/
#                                                 temp['Adj Close'].shift(252))
#            
#            temp['Rolling52wkStandardDeviation'] = temp['LogRet'].rolling(
#                                            center = False, window = 252).std()
#            
#            temp['Rolling4wkStandardDeviation'] = temp['LogRet'].rolling(
#                                             center = False, window = 20).std()
#            
#            temp['AverageAnnualRollingVolume'] = temp['Volume'].rolling(
#                                               center=False, window=252).mean()
#            
#            temp['Rolling52wkCoefficientOfVariation'] = (
#                temp['Rolling52wkStandardDeviation']/temp['Rolling52wkReturn'])
#            
#            temp['Rolling52wkDoubleStandardDeviation'] = (
#                temp['Rolling52wkStandardDeviation'].rolling(
#                center = False, window = 252))
#            
#            temp['4wkOver52wkStandardDeviationRatio'] = (
#                temp['Rolling4wkStandardDeviation']/temp['Rolling52wkStandardDeviation'])    
#            
#            # ADX with PDI, MDI, ADX, ADXmean, TrueRange, AverageTrueRange, ADXStrength
#            ADXwindow = 14
#            temp['ADXUpMove'] = temp['High'] - temp['High'].shift(1)
#            temp['ADXDownMove'] = temp['Low'] - temp['Low'].shift(1)
#            temp['Method1'] = temp['High'] - temp['Low']
#            temp['Method2'] = abs((temp['High'] - temp['Adj Close'].shift(1)))
#            temp['Method3'] = abs((temp['Low'] - temp['Adj Close'].shift(1)))
#            temp['Method1'] = temp['Method1'].fillna(0)
#            temp['Method2'] = temp['Method2'].fillna(0)
#            temp['Method3'] = temp['Method3'].fillna(0)
#            temp['TrueRange'] = temp[['Method1','Method2','Method3']].max(axis = 1)
#            temp['AverageTrueRange'] = temp['TrueRange'].rolling(window = ADXwindow,
#                                            center=False).sum()
#            temp['AverageTrueRange'] = ((temp['AverageTrueRange'].shift(1)*(ADXwindow-1
#                                         ) + temp['TrueRange']) / ADXwindow)
#            temp['PDM'] = (temp['High'] - temp['High'].shift(1))
#            temp['MDM'] = (temp['Low'].shift(1) - temp['Low'])
#            temp['PDM'] = temp['PDM'][temp['PDM'] > 0]
#            temp['MDM'] = temp['MDM'][temp['MDM'] > 0]
#            temp['PDM'] = temp['PDM'].fillna(0)
#            temp['MDM'] = temp['MDM'].fillna(0)
#            temp['SmoothPDM'] = temp['PDM'].rolling(window = ADXwindow,
#                                            center=False).sum()
#            temp['SmoothPDM'] = ((temp['SmoothPDM'].shift(1)*(ADXwindow-1
#                                         ) + temp['PDM']) / ADXwindow)
#            temp['SmoothMDM'] = temp['MDM'].rolling(window = ADXwindow,
#                                            center=False).sum()
#            temp['SmoothMDM'] = ((temp['SmoothMDM'].shift(1)*(ADXwindow-1
#                                         ) + temp['MDM']) / ADXwindow)
#            temp['PDI'] = (100*(temp['SmoothPDM']/temp['AverageTrueRange']))
#            temp['MDI'] = (100*(temp['SmoothMDM']/temp['AverageTrueRange']))
#            temp['DIdiff'] = abs(temp['PDI'] - temp['MDI'])
#            temp['DIsum'] = temp['PDI'] + temp['MDI']
#            temp['DX'] = (100 * (temp['DIdiff']/temp['DIsum']))
#            temp['ADX'] = temp['DX'].rolling(window = ADXwindow, center = False).mean()
#            temp['DIdivergence'] = temp['PDI'] - temp['MDI']
#            temp['ADXMean'] = temp['ADX'].mean() * .9 #Scaling factor
#            temp['ADXStrength'] = temp['ADX']/temp['ADXMean']
#            
#            #Ballerbands Lower/Upperband, bandwidth, b%
#            BBwindow = 20
#            temp['nDaySMA'] = temp['Adj Close'].rolling(window=BBwindow, center=False).mean()
#            temp['nDaySTD'] = temp['Adj Close'].rolling(window=BBwindow, center=False).std()
#            temp['UpperBand'] = temp['nDaySMA'] + (temp['nDaySTD'] * 2)
#            temp['LowerBand'] = temp['nDaySMA'] - (temp['nDaySTD'] * 2)
#            temp['BandWidth'] = ((temp['UpperBand'] - temp['LowerBand'])/temp['nDaySMA'])*100
#            temp['B'] = (temp['Adj Close'] - temp['LowerBand'])/(temp['UpperBand'] - temp['LowerBand'])
#            
#            #Chaikin Money Flow MFMultiplier, CMF (CMF - need to normalize or make rolling sum)
#            CMFwindow = 20
#            temp['MFMultiplier'] = (((temp['Adj Close'] - temp['Low']) - (temp['High'] 
#            - temp['Adj Close'])) / (temp['High'] - temp['Low']))
#            temp['MFVolume'] = (temp['Volume'] * temp['MFMultiplier'])
#            temp['ZeroLine'] = 0
#            temp['CMF'] = temp['MFVolume'].rolling(center=False, window=CMFwindow).sum(
#                    )/temp['Volume'].rolling(center=False, window=CMFwindow).sum()
#            
#            #Commodity Channel Index
#            constant = .02
#            CCIwindow = 20 
#            temp['TP'] = (temp['High'] + temp['Low'] + temp['Adj Close']) / 3
#            temp['TPSMA'] = temp['TP'].rolling(center=False, window = CCIwindow).mean()
#            temp['MeanDeviation'] = temp['TP'].rolling(center=False, window = CCIwindow).std()
#            temp['CCI'] = ((temp['TP'] - temp['TPSMA'])/(constant*temp['MeanDeviation']))
#            temp['Top'] = 100
#            temp['Bottom'] = -100
#            
#            #Day over average rolling volume DayOverARV
#            DayOverwindow = 60
#            temp['AverageRollingVolume'] = temp['Volume'].rolling(center=False, 
#                                                                window=DayOverwindow).mean() 
#            temp['DayOverARV'] = temp['Volume']/temp['AverageRollingVolume'] 
#            
#            #Simple Moving Average
#            littlewindow = 20 #number of days for moving average window
#            bigwindow = 252 #numer of days for moving average window
#            temp['SmallSMA'] = temp['Adj Close'].rolling(window=littlewindow, center=False).mean()
#            temp['LargeSMA'] = temp['Adj Close'].rolling(window=bigwindow, center=False).mean()
#            temp['4wkOver52wk'] = (temp['SmallSMA'] - temp['LargeSMA'])/temp['Adj Close']
#            temp['priceOver4wk'] = (temp['Adj Close'] - temp['SmallSMA'])/temp['Adj Close']
#            #RSI
#            closeprice = temp['Adj Close']
#            RSIwindow = 14  
#            change = closeprice.diff()
#            change = change[1:]
#            up, down = change.copy(), change.copy()
#            up[up < 0] = 0
#            down[down > 0] = 0
#            AvgGain = up.rolling(RSIwindow).mean()
#            AvgGain = AvgGain.fillna(0)
#            AvgLoss = down.abs().rolling(RSIwindow).mean()
#            AvgLoss = AvgLoss.fillna(0)
#            RS = AvgGain/AvgLoss
#            RS = RS.fillna(0)
#            RSI = 100 - (100/(1.0+RS))
#            temp['RSI'] = pd.Series(RSI)
#            
#            #Gap Up
#            temp['GapUp'] = (temp['High'].shift(1) - temp['Low']) / temp['Adj Close'].shift(1)
#            temp['GapUp'] = temp['GapUp'][temp['GapUp'] < 0]
#            temp['GapUp'] = temp['GapUp'].fillna(0)
#            temp['GapUp'] = np.where(temp['GapUp'] == 0 , 0, (-1*temp['GapUp']))
#            
#            #Gap Down
#            temp['GapDown'] = (temp['Low'].shift(1) - temp['High']) / temp['Adj Close'].shift(1)
#            temp['GapDown'] = temp['GapDown'][temp['GapDown'] > 0]
#            temp['GapDown'] = temp['GapDown'].fillna(0)
#            
#            #Rate of Change
#            lag = 12
#            temp['RateOfChange'] = (temp['Adj Close'] - temp['Adj Close'].shift(lag)
#                                              ) / temp['Adj Close'].shift(lag)         
#               
#    #           #temp = temp.drop('column_name', axis =  1) #drop function
            #Delete duplicate rows
            temp = temp[~temp.index.duplicated(keep='first')]
            #Save to pickle
            pd.to_pickle(temp, 'F:\\Users\\UserName\\DirectoryLocation\\' +
                        CSVlist[ii][:-4] + '\\' + CSVlist[ii][:-4])
    except OSError:
        continue

#Stop timers
end = t.time()
end1 = t.time()
#Timer stats
print('Reupdate across nonstandard columns took' + str(end - start) + 'seconds')
print('Whole script took' + str(end1 - start1) +'seconds')
