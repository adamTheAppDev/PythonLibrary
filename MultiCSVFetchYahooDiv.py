# -*- coding: utf-8 -*-
"""
Created on Fri May 19 16:53:41 2017

@author: AmatVictoriaCuramIII
"""

#This is an HTML scraper and formatting tool for dividend time series database construction

from pandas import read_csv 
import requests
import pandas as pd
import os
import time
from io import StringIO
from CrumbCatcher import CrumbCatcher
from pandas.parser import CParserError
#df = read_csv('refdfser.csv', sep = ',')
df = pd.read_pickle('C:\\Users\\AmatVictoriaCuramIII\\Desktop\\Python\\Universe2018')

#symbol = df.Symbol.values
ranger = range(0,len(df))
for i in ranger[:5]:
    try: 
        ticker = str(df[i][:-4])
        artificialcrumb = CrumbCatcher(ticker)        
        downloadurl = ("https://query1.finance.yahoo.com/v7/finance/download/" + ticker 
        + "?period1=-631123200&period2=1598374000&interval=1d&events=div&crumb=" + artificialcrumb)
        mainurl = ("https://finance.yahoo.com/quote/" + ticker + "/history?p=" + ticker)
        response = requests.post(downloadurl)#, data=CookieDict)
        datastr = response.text
        formatter = StringIO(datastr)
        strdf = pd.read_csv(formatter, sep = ',')
        if strdf.columns[0] == '{"chart":{"result":null':
            print('The URL failed for ' + ticker)
            continue
        strdf = strdf.set_index('Date')
        strdf.index = pd.to_datetime(strdf.index, format = "%Y/%m/%d") 
        if len(strdf) == 0:
            print("No dividend history for " + str(df[i][:-4]) )
            continue
        strdf.to_csv(("F:\\Users\\AmatVictoriaCuram\\TemporaryCSV\\"+ ticker + "div.csv"))
        print(ticker)
        continue
    except CParserError:
        print('Parser failed for ' + ticker)
        continue
    except ConnectionError:
        try:
            #Sleep, then retry last ticker, continue loop.
            print('ConnectionError on ' + str(ticker) + '.')
            print('Sleeping for 5 min.')        
            time.sleep(301)
            print('Parsing for ' + ticker + '.')
            #Retrying parse
            artificialcrumb = CrumbCatcher(ticker)        
            downloadurl = ("https://query1.finance.yahoo.com/v7/finance/download/" + ticker 
            + "?period1=-631123200&period2=1598374000&interval=1d&events=div&crumb=" + artificialcrumb)
            mainurl = ("https://finance.yahoo.com/quote/" + ticker + "/history?p=" + ticker)
            response = requests.post(downloadurl)#, data=CookieDict)
            datastr = response.text
            formatter = StringIO(datastr)
            strdf = pd.read_csv(formatter, sep = ',')
            if strdf.columns[0] == '{"chart":{"result":null':
                print('The URL failed for ' + ticker)
                continue
            strdf = strdf.set_index('Date')
            strdf.index = pd.to_datetime(strdf.index, format = "%Y/%m/%d") 
            strdf.to_csv(("F:\\Users\\AmatVictoriaCuram\\TemporaryCSV\\"+ ticker + "div.csv"))
            print(ticker)
            continue
        except CParserError:
            print('Parser failed for ' + ticker + '.')
            continue
        except requests.exceptions.SSLError:
            try:
                print('SSLError after Connection Error for ' + ticker + '.')
                #Sleep, then retry last ticker, continue loop.
                print('Sleeping for 61 seconds.')        
                time.sleep(61)
                print('Parsing for ' + ticker + '.')
                #Retrying parse
                artificialcrumb = CrumbCatcher(ticker)        
                downloadurl = ("https://query1.finance.yahoo.com/v7/finance/download/" + ticker 
                + "?period1=-631123200&period2=1598374000&interval=1d&events=div&crumb=" + artificialcrumb)
                mainurl = ("https://finance.yahoo.com/quote/" + ticker + "/history?p=" + ticker)
                response = requests.post(downloadurl)#, data=CookieDict)
                datastr = response.text
                formatter = StringIO(datastr)
                strdf = pd.read_csv(formatter, sep = ',')
                if strdf.columns[0] == '{"chart":{"result":null':
                    print('The URL failed for ' + ticker)
                    continue
                strdf = strdf.set_index('Date')
                strdf.index = pd.to_datetime(strdf.index, format = "%Y/%m/%d") 
                strdf.to_csv(("F:\\Users\\AmatVictoriaCuram\\TemporaryCSV\\"+ ticker + "div.csv"))
                print(ticker)
                continue   
            except CParserError:
                print('Parser failed for ' + ticker + '.')
                continue
            except requests.exceptions.SSLError:
                print('Double SSLError after ConnectionError for ' + ticker + '.')
                continue            
            except ConnectionError:
                print('Double ConnectionError for ' + ticker + '.')
                continue
    except requests.exceptions.SSLError:
        try:
            #Sleep, then retry last ticker, continue loop.
            print('SSLError on ' + str(ticker) + '.')
            print('Sleeping for 61 seconds.')        
            time.sleep(61)
            print('Parsing for ' + ticker + '.')
            #Retrying parse
            artificialcrumb = CrumbCatcher(ticker)        
            downloadurl = ("https://query1.finance.yahoo.com/v7/finance/download/" + ticker 
            + "?period1=-631123200&period2=1598374000&interval=1d&events=div&crumb=" + artificialcrumb)
            mainurl = ("https://finance.yahoo.com/quote/" + ticker + "/history?p=" + ticker)
            response = requests.post(downloadurl)#, data=CookieDict)
            datastr = response.text
            formatter = StringIO(datastr)
            strdf = pd.read_csv(formatter, sep = ',')
            if strdf.columns[0] == '{"chart":{"result":null':
                print('The URL failed for ' + ticker)
                continue
            strdf = strdf.set_index('Date')
            strdf.index = pd.to_datetime(strdf.index, format = "%Y/%m/%d") 
            strdf.to_csv(("F:\\Users\\AmatVictoriaCuram\\TemporaryCSV\\"+ ticker + "div.csv"))
            print(ticker)
            continue
        except CParserError:
            print('Parser failed for ' + ticker + '.')
            continue
        except requests.exceptions.SSLError:
            print('Double SSLError for ' + ticker + '.')
            continue
        except ConnectionError:
            try:
                #Sleep, then retry last ticker, continue loop.
                print('ConnectionError after SSLError on ' + str(ticker) + '.')
                print('Sleeping for 61 seconds.')        
                time.sleep(61)
                print('Parsing for ' + ticker + '.')
                #Retrying parse
                artificialcrumb = CrumbCatcher(ticker)        
                downloadurl = ("https://query1.finance.yahoo.com/v7/finance/download/" + ticker 
                + "?period1=-631123200&period2=1598374000&interval=1d&events=div&crumb=" + artificialcrumb)
                mainurl = ("https://finance.yahoo.com/quote/" + ticker + "/history?p=" + ticker)
                response = requests.post(downloadurl)#, data=CookieDict)
                datastr = response.text
                formatter = StringIO(datastr)
                strdf = pd.read_csv(formatter, sep = ',')
                if strdf.columns[0] == '{"chart":{"result":null':
                    print('The URL failed for ' + ticker)
                    continue
                strdf = strdf.set_index('Date')
                strdf.index = pd.to_datetime(strdf.index, format = "%Y/%m/%d") 
                strdf.to_csv(("F:\\Users\\AmatVictoriaCuram\\TemporaryCSV\\"+ ticker + "div.csv"))
                print(ticker)
                continue
            except CParserError:
                print('Parser failed after SSLError and ConnectionError for ' + ticker + '.')
                continue
            except requests.exceptions.SSLError:
                print('SSLError after SSLError and ConnectionEror for ' + ticker + '.')
                continue

#location = 'F:/Users/AmatVictoriaCuram/TemporaryCSV'
#midlist = os.listdir(location)
#idle1 = 0
#if len(midlist) > 0:
#    endlist = [x[:-7] for x in midlist]
#    startlist = list(df['Symbol'])
#    Needed = [x for x in startlist if x not in endlist]
#    needf = pd.DataFrame(Needed, columns=['Symbol'])
#    ranger1 = range(0,len(needf))
#    for j in ranger1:
#        try:
#            ticker = needf['Symbol'][j]
#            downloadurl = ("https://query1.finance.yahoo.com/v7/finance/download/" + ticker 
#            + "?period1=-631123200&period2=1598374000&interval=1d&events=div&crumb=" + artificialcrumb)
#            response = requests.post(downloadurl)#, data=CookieDict)
#            datastr = response.text
#            formatter = StringIO(datastr)
#            strdf = pd.read_csv(formatter, sep = ',')
#            if strdf.columns[0] == '{"chart":{"result":null':
#                print('The URL failed for ' + ticker)                
#                continue
#            strdf = strdf.set_index('Date')
#            strdf.index = pd.to_datetime(strdf.index, format = "%Y/%m/%d") 
#            print(ticker)
#            strdf.to_csv(("F:\\Users\\AmatVictoriaCuram\\TemporaryCSV\\"+ ticker + "div.csv"))
#        except CParserError:
#            print("The parser failed for" + ticker)
#            continue
#        
#            
#newmidlist = os.listdir(location)
#newendlist = [x[:-7] for x in newmidlist]
#newNeeded = [x for x in startlist if x not in newendlist]
#print(str(len(newNeeded)) + ' Unimported Stocks Exist')
#
