# -*- coding: utf-8 -*-
"""
Created on Fri May 19 16:53:41 2017

@author: AmatVictoriaCuramIII
"""
#import urllib
#import webbrowser as web
from pandas import read_csv 
import requests
#import time as time
#import re
import pandas as pd
#import io
import os
from io import StringIO
from pandas.parser import CParserError
df = read_csv('goodsymbols.csv', sep = ',')
symbol = df.Symbol.values
ranger = range(0,len(df))
artificialcrumb = "M1Wvnw0F19W"
for i in ranger:
    try: 
        ticker = str(df.Symbol[i])
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
    except CParserError:
        print('Parser failed for ' + ticker)
        continue    
    # you may now write to file

location = 'F:/Users/AmatVictoriaCuram/TemporaryCSV'
midlist = os.listdir(location)
idle1 = 0
if len(midlist) > 0:
    endlist = [x[:-7] for x in midlist]
    startlist = list(df['Symbol'])
    Needed = [x for x in startlist if x not in endlist]
    needf = pd.DataFrame(Needed, columns=['Symbol'])
    ranger1 = range(0,len(needf))
    for j in ranger1:
        try:
            ticker = df['Symbol'][j]
            downloadurl = ("https://query1.finance.yahoo.com/v7/finance/download/" + ticker 
            + "?period1=-631123200&period2=1598374000&interval=1d&events=div&crumb=" + artificialcrumb)
            response = requests.post(downloadurl)#, data=CookieDict)
            datastr = response.text
            formatter = StringIO(datastr)
            strdf = pd.read_csv(formatter, sep = ',')
            if strdf.columns[0] == '{"chart":{"result":null':
                print('The URL failed for ' + ticker)                
                continue
            strdf = strdf.set_index('Date')
            strdf.index = pd.to_datetime(strdf.index, format = "%Y/%m/%d") 
            print(ticker)
            strdf.to_csv(("F:\\Users\\AmatVictoriaCuram\\TemporaryCSV\\"+ ticker + "div.csv"))
        except CParserError:
            print("The parser failed for" + ticker)
            continue
        
            
newmidlist = os.listdir(location)
newendlist = [x[:-7] for x in newmidlist]
newNeeded = [x for x in startlist if x not in newendlist]
print(str(len(newNeeded)) + ' Unimported Stocks Exist')

