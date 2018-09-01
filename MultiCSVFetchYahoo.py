 # -*- coding: utf-8 -*-
"""
Created on Fri May 19 16:53:41 2017

@author: AmatVictoriaCuramIII
"""

from pandas import read_csv 
import requests
import pandas as pd
import os
import time
from io import StringIO
from pandas.parser import CParserError
df = read_csv('goodsymbols.csv', sep = ',')
df1 = df.set_index('Symbol')
symbol = df.Symbol.values
firsthalf = "https://query1.finance.yahoo.com/v7/finance/download/" #insert ticker and add secondhalf
secondhalf = "?period1=-630950400&period2=1592694000&interval=1d&events=history&crumb=1.ZWRp1I9ZS" #1950 - most recent
nocrumb = "?period1=-630950400&period2=1592694000&interval=1d&events=history&crumb="
df['URL'] = firsthalf + df['Symbol'] + secondhalf

ranger = range(0,len(df))
artificialcrumb = "1.ZWRp1I9ZS"
for i in ranger:
    try: 
        ticker = str(df.Symbol[i])
        time.sleep(2)
        downloadurl = ("https://query1.finance.yahoo.com/v7/finance/download/" + ticker 
        + "?period1=-631123200&period2=1598374000&interval=1d&events=history&crumb=" + artificialcrumb)
        response = requests.post(downloadurl)#, data=CookieDict)
        datastr = response.text
        formatter = StringIO(datastr)
        strdf = pd.read_csv(formatter, sep = ',')
        if strdf.columns[0] == '{"chart":{"result":null':
            print('The URL failed for ' + ticker)
            continue
        strdf = strdf.set_index('Date')
        strdf.index = pd.to_datetime(strdf.index, format = "%Y/%m/%d") 
        strdf.to_csv(("F:\\Users\\AmatVictoriaCuram\\TemporaryCSV\\"+ ticker + ".csv"))
        print(ticker)
    except CParserError:
        print('Parser failed for ' + ticker)
        continue    
    # you may now write to file

location = 'F:/Users/AmatVictoriaCuram/TemporaryCSV'
midlist = os.listdir(location)
idle1 = 0
if len(midlist) > 0:
    endlist = [x[:-4] for x in midlist]
    startlist = list(df['Symbol'])
    Needed = [x for x in startlist if x not in endlist]
    needf = pd.DataFrame(Needed, columns=['Symbol'])
    ranger1 = range(0,len(needf))
    for j in ranger1:
        try:
            ticker = df['Symbol'][j]
            downloadurl = ("https://query1.finance.yahoo.com/v7/finance/download/" + ticker 
            + "?period1=-631123200&period2=1598374000&interval=1d&events=history&crumb=" + artificialcrumb)
            mainurl = "https://finance.yahoo.com/quote/" + ticker + "/history?p=" + ticker
            response = requests.post(downloadurl)#, data=CookieDict)
            datastr = response.text
            formatter = StringIO(datastr)
            strdf = pd.read_csv(formatter, sep = ',')
            if strdf.columns[0] == '{"chart":{"result":null':
                print('The URL failed for ' + ticker)                
                continue
            strdf = strdf.set_index('Date')
            strdf.index = pd.to_datetime(strdf.index, format = "%Y/%m/%d") 
            strdf.to_csv(("F:\\Users\\AmatVictoriaCuram\\TemporaryCSV\\"+ ticker + ".csv"))
        except CParserError:
            print("The parser failed for" + ticker)
            continue
        
            
newmidlist = os.listdir(location)
newendlist = [x[:-4] for x in newmidlist]
newNeeded = [x for x in startlist if x not in newendlist]
print(str(len(newNeeded)) + ' Unimported Stocks Exist')

