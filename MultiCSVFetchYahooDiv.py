# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is an HTML scraper and formatting tool for dividend time series database construction

#Import modules
from pandas import read_csv 
import requests
import pandas as pd
import os
import time
from io import StringIO
from CrumbCatcher import CrumbCatcher
from pandas.parser import CParserError

#Read in data
#df = read_csv('refdfser.csv', sep = ',')
df = pd.read_pickle('C:\\Users\\AmatVictoriaCuramIII\\Desktop\\Python\\Universe2018')

#symbol = df.Symbol.values
#Iterable
ranger = range(0,len(df))
#For number of tickers
for i in ranger[:5]:
    try: 
        #Assign ticker
        ticker = str(df[i][:-4])
        #Generate crumb
        artificialcrumb = CrumbCatcher(ticker)     
        #Generate download url
        downloadurl = ("https://query1.finance.yahoo.com/v7/finance/download/" + ticker 
        + "?period1=-631123200&period2=1598374000&interval=1d&events=div&crumb=" + artificialcrumb)
        #Line optional
        mainurl = ("https://finance.yahoo.com/quote/" + ticker + "/history?p=" + ticker)
        #Get response
        response = requests.post(downloadurl)#, data=CookieDict)
        #Format text
        datastr = response.text
        formatter = StringIO(datastr)
        strdf = pd.read_csv(formatter, sep = ',')
        #If bad response
        if strdf.columns[0] == '{"chart":{"result":null':
            print('The URL failed for ' + ticker)
            continue
        #Format date index    
        strdf = strdf.set_index('Date')
        strdf.index = pd.to_datetime(strdf.index, format = "%Y/%m/%d") 
        if len(strdf) == 0:
            print("No dividend history for " + str(df[i][:-4]) )
            continue
        #Save to CSV
        strdf.to_csv(("F:\\Users\\AmatVictoriaCuram\\TemporaryCSV\\"+ ticker + "div.csv"))
        #Iteration tracking
        print(ticker)
        continue
    #Bad response
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
            #Generate crumb
            artificialcrumb = CrumbCatcher(ticker)      
            #Generate download url
            downloadurl = ("https://query1.finance.yahoo.com/v7/finance/download/" + ticker 
            + "?period1=-631123200&period2=1598374000&interval=1d&events=div&crumb=" + artificialcrumb)
            #Line optional
            mainurl = ("https://finance.yahoo.com/quote/" + ticker + "/history?p=" + ticker)
            #Get response
            response = requests.post(downloadurl)#, data=CookieDict)
            #Format text
            datastr = response.text
            formatter = StringIO(datastr)
            strdf = pd.read_csv(formatter, sep = ',')
            #If bad response
            if strdf.columns[0] == '{"chart":{"result":null':
                print('The URL failed for ' + ticker)
                continue
            #Format date index    
            strdf = strdf.set_index('Date')
            strdf.index = pd.to_datetime(strdf.index, format = "%Y/%m/%d") 
            #Save to CSV
            strdf.to_csv(("F:\\Users\\AmatVictoriaCuram\\TemporaryCSV\\"+ ticker + "div.csv"))
            #Iteration tracking
            print(ticker)
            continue
        #Bad response
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
                #Generate crumb
                artificialcrumb = CrumbCatcher(ticker)   
                #Generate download url
                downloadurl = ("https://query1.finance.yahoo.com/v7/finance/download/" + ticker 
                + "?period1=-631123200&period2=1598374000&interval=1d&events=div&crumb=" + artificialcrumb)
                #Line optional
                mainurl = ("https://finance.yahoo.com/quote/" + ticker + "/history?p=" + ticker)
                #Get response
                response = requests.post(downloadurl)#, data=CookieDict)
                #Format text
                datastr = response.text
                formatter = StringIO(datastr)
                strdf = pd.read_csv(formatter, sep = ',')
                #If bad response
                if strdf.columns[0] == '{"chart":{"result":null':
                    print('The URL failed for ' + ticker)
                    continue
                #Format date index    
                strdf = strdf.set_index('Date')
                strdf.index = pd.to_datetime(strdf.index, format = "%Y/%m/%d") 
                #Save to CSV
                strdf.to_csv(("F:\\Users\\AmatVictoriaCuram\\TemporaryCSV\\"+ ticker + "div.csv"))
                #Iteration tracking
                print(ticker)
                continue   
            #Bad response
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
            #Generate crumb
            artificialcrumb = CrumbCatcher(ticker)    
            #Generate download url
            downloadurl = ("https://query1.finance.yahoo.com/v7/finance/download/" + ticker 
            + "?period1=-631123200&period2=1598374000&interval=1d&events=div&crumb=" + artificialcrumb)
            #Line optional
            mainurl = ("https://finance.yahoo.com/quote/" + ticker + "/history?p=" + ticker)
            #Get response
            response = requests.post(downloadurl)#, data=CookieDict)
            #Format text
            datastr = response.text
            formatter = StringIO(datastr)
            strdf = pd.read_csv(formatter, sep = ',')
            #If bad response
            if strdf.columns[0] == '{"chart":{"result":null':
                print('The URL failed for ' + ticker)
                continue
            #Format date index    
            strdf = strdf.set_index('Date')
            strdf.index = pd.to_datetime(strdf.index, format = "%Y/%m/%d") 
            #Save to CSV
            strdf.to_csv(("F:\\Users\\AmatVictoriaCuram\\TemporaryCSV\\"+ ticker + "div.csv"))
            #Iteration tracking
            print(ticker)
            continue
        #Bad response
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
                #Generate crumb
                artificialcrumb = CrumbCatcher(ticker)       
                #Generate download url
                downloadurl = ("https://query1.finance.yahoo.com/v7/finance/download/" + ticker 
                + "?period1=-631123200&period2=1598374000&interval=1d&events=div&crumb=" + artificialcrumb)
                #Line optional
                mainurl = ("https://finance.yahoo.com/quote/" + ticker + "/history?p=" + ticker)
                #Get response
                response = requests.post(downloadurl)#, data=CookieDict)
                #Format text
                datastr = response.text
                formatter = StringIO(datastr)
                strdf = pd.read_csv(formatter, sep = ',')
                #If bad response
                if strdf.columns[0] == '{"chart":{"result":null':
                    print('The URL failed for ' + ticker)
                    continue
                #Format date index
                strdf = strdf.set_index('Date')
                strdf.index = pd.to_datetime(strdf.index, format = "%Y/%m/%d") 
                #Save to CSV
                strdf.to_csv(("F:\\Users\\AmatVictoriaCuram\\TemporaryCSV\\"+ ticker + "div.csv"))
                #Iteration tracking
                print(ticker)
                continue
            #Bad response    
            except CParserError:
                print('Parser failed after SSLError and ConnectionError for ' + ticker + '.')
                continue
            except requests.exceptions.SSLError:
                print('SSLError after SSLError and ConnectionEror for ' + ticker + '.')
                continue
