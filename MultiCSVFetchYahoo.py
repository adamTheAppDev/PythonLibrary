# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is an HTML scraper and formatting tool for time series database construction

#Import modules
from pandas import read_csv 
import requests
import pandas as pd
import os
import time
from io import StringIO
from CrumbCatcher import CrumbCatcher
from pandas.parser import CParserError
from requests.exceptions import ConnectionError

#Read in data
#df = read_csv('refdfser.csv', sep = ',')
df = pd.read_pickle('C:\\Users\\AmatVictoriaCuramIII\\Desktop\\Python\\Universe2018')
#ticker finder
#df['Symbol'][df['Symbol'] == '^AEX'].index
#trim and reset index if interrupted
df = df[4212:]
#df = df.reset_index(drop=True)

#Unneccessary code
firsthalf = "https://query1.finance.yahoo.com/v7/finance/download/" #insert ticker and add secondhalf
secondhalf = "?period1=-630950400&period2=1592694000&interval=1d&events=history&crumb=1.ZWRp1I9ZS" #1950 - most recent
nocrumb = "?period1=-630950400&period2=1592694000&interval=1d&events=history&crumb="
#df['URL'] = firsthalf + df['Symbol'] + secondhalf

#https://query1.finance.yahoo.com/v7/finance/download/%5EGSPC?period1=-631123200&period2=1542873600&interval=1wk&events=history&crumb=DoJbYX/6Mee

#Iterable
ranger = range(0,len(df))
#artificialcrumb = str(CrumbCatcher(ticker))
#For number of tickers
for i in ranger:
    try: 
        #Assign ticker
        ticker = str(df[i][:-4])
#        time.sleep(2)
        #Generate crumb
        artificialcrumb = str(CrumbCatcher(str(ticker)))
        #Generate download url
        downloadurl = ("https://query1.finance.yahoo.com/v7/finance/download/" + ticker 
        + "?period1=-631123200&period2=1598374000&interval=1d&events=history&crumb=" + artificialcrumb)
    
        #Get response
        response = requests.post(downloadurl)#, data=CookieDict)
        #Format text
        datastr = response.text
        formatter = StringIO(datastr)
        strdf = pd.read_csv(formatter, sep = ',')
 
        #Bad response
        if strdf.columns[0] == '{"chart":{"result":null':
            print('The URL failed for ' + ticker)
            continue
      
        #Set date as index
        strdf = strdf.set_index('Date')
        #Format date
        strdf.index = pd.to_datetime(strdf.index, format = "%Y/%m/%d") 
        
        #Save to CSV
        strdf.to_csv(("F:\\Users\\AmatVictoriaCuram\\TemporaryCSV\\" + ticker + ".csv"))
        #Iteration tracking
        print(ticker)
        continue
    #From bad response
    except CParserError:
        print('Parser failed for ' + ticker)
        continue
    #From timeout
    except ConnectionError:
        try:
            #Sleep, then retry last ticker, continue loop.
            print('ConnectionError on ' + str(ticker) + '.')
            print('Sleeping for 5 min.')        
            time.sleep(301)
            #Retrying parse
            print('Parsing for ' + ticker + '.')
            
            #Generate crumb
            artificialcrumb = str(CrumbCatcher(str(ticker)))
            #Generate download url
            downloadurl = ("https://query1.finance.yahoo.com/v7/finance/download/" + ticker 
            + "?period1=-631123200&period2=1598374000&interval=1d&events=history&crumb=" + artificialcrumb)
            
            #Get response
            response = requests.post(downloadurl)#, data=CookieDict)
            #Format text
            datastr = response.text
            formatter = StringIO(datastr)
            strdf = pd.read_csv(formatter, sep = ',')
            
            #Bad response
            if strdf.columns[0] == '{"chart":{"result":null':
                print('The URL failed for ' + ticker)
                continue
               
            #Set date as index   
            strdf = strdf.set_index('Date')
            #Format date
            strdf.index = pd.to_datetime(strdf.index, format = "%Y/%m/%d") 
            
            #Save to CSV
            strdf.to_csv(("F:\\Users\\AmatVictoriaCuram\\TemporaryCSV\\" + ticker + ".csv"))
            #Iteration tracking
            print(ticker)
            #Moving on to next ticker
            continue
        #From bad response    
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
                artificialcrumb = str(CrumbCatcher(str(ticker)))
                #Generate download url
                downloadurl = ("https://query1.finance.yahoo.com/v7/finance/download/" + ticker 
                + "?period1=-631123200&period2=1598374000&interval=1d&events=history&crumb=" + artificialcrumb)
                
                #Get response
                response = requests.post(downloadurl)#, data=CookieDict)
                #Format text
                datastr = response.text
                formatter = StringIO(datastr)
                strdf = pd.read_csv(formatter, sep = ',')
                
                #Bad response
                if strdf.columns[0] == '{"chart":{"result":null':
                    print('The URL failed for ' + ticker)
                    continue
                   
                #Set date as index   
                strdf = strdf.set_index('Date')
                #Format date
                strdf.index = pd.to_datetime(strdf.index, format = "%Y/%m/%d") 
                
                #Save to CSV
                strdf.to_csv(("F:\\Users\\AmatVictoriaCuram\\TemporaryCSV\\" + ticker + ".csv"))
                #Iteration tracking
                print(ticker)
                #Moving on to next ticker
                continue    
            #From bad response    
            except CParserError:
                print('Parser failed for ' + ticker + '.')
                continue
            except requests.exceptions.SSLError:
                print('Double SSLError after ConnectionError for ' + ticker + '.')
                continue            
            #From timeout   
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
            artificialcrumb = str(CrumbCatcher(str(ticker)))
            #Generate download url
            downloadurl = ("https://query1.finance.yahoo.com/v7/finance/download/" + ticker 
            + "?period1=-631123200&period2=1598374000&interval=1d&events=history&crumb=" + artificialcrumb)
            
            #Get response
            response = requests.post(downloadurl)#, data=CookieDict)
            #Format text
            datastr = response.text
            formatter = StringIO(datastr)
            strdf = pd.read_csv(formatter, sep = ',')
            #Bad response
            if strdf.columns[0] == '{"chart":{"result":null':
                print('The URL failed for ' + ticker)
                continue

            #Set date as index   
            strdf = strdf.set_index('Date')
            #Format date
            strdf.index = pd.to_datetime(strdf.index, format = "%Y/%m/%d") 
            
            #Save to CSV
            strdf.to_csv(("F:\\Users\\AmatVictoriaCuram\\TemporaryCSV\\" + ticker + ".csv"))
            #Iteration tracking
            print(ticker)
            #Moving on to next ticker
            continue    
        #From bad response    
        except CParserError:
            print('Parser failed for ' + ticker + '.')
            continue
        except requests.exceptions.SSLError:
            print('Double SSLError for ' + ticker + '.')
            continue
        #From timeout   
        except ConnectionError:
            try:
                #Sleep, then retry last ticker, continue loop.
                print('ConnectionError after SSLError on ' + str(ticker) + '.')
                print('Sleeping for 61 seconds.')        
                time.sleep(61)
                print('Parsing for ' + ticker + '.')
                #Retrying parse
                
                #Generate crumb
                artificialcrumb = str(CrumbCatcher(str(ticker)))
                #Generate download url
                downloadurl = ("https://query1.finance.yahoo.com/v7/finance/download/" + ticker 
                + "?period1=-631123200&period2=1598374000&interval=1d&events=history&crumb=" + artificialcrumb)
                
                #Get response
                response = requests.post(downloadurl)#, data=CookieDict)
                #Format text
                datastr = response.text
                formatter = StringIO(datastr)
                strdf = pd.read_csv(formatter, sep = ',')
                
                #Bad response
                if strdf.columns[0] == '{"chart":{"result":null':
                    print('The URL failed for ' + ticker)
                    continue
                   
                #Set date as index
                strdf = strdf.set_index('Date')
                #Format date
                strdf.index = pd.to_datetime(strdf.index, format = "%Y/%m/%d") 
                
                #Save to CSV
                strdf.to_csv(("F:\\Users\\AmatVictoriaCuram\\TemporaryCSV\\" + ticker + ".csv"))
                #Iteration tracking
                print(ticker)
                #Moving on to next ticker
                continue
            #From bad response    
            except CParserError:
                print('Parser failed after SSLError and ConnectionError for ' + ticker + '.')
                continue
            except requests.exceptions.SSLError:
                print('SSLError after SSLError and ConnectionEror for ' + ticker + '.')
                continue  
               
#Directory location    
location = 'F:/Users/Username/TemporaryCSVLocation'
#List files in directory
midlist = os.listdir(location)
newmidlist = os.listdir(location)
#Strip '.csv'
newendlist = [x[:-4] for x in newmidlist]
#Tickers that did not make save to file
newNeeded = [x for x in startlist if x not in newendlist]
#Display results
print(str(len(newNeeded)) + ' Unimported Stocks Exist')
