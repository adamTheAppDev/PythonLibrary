# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 13:21:43 2017

@author: AmatVictoriaCuramIII
"""

#YahooGrabber
def YahooDivGrabber(ticker):
    import requests
    from io import StringIO
    import pandas as pd
    import time as t
    from CrumbCatcher import CrumbCatcher
    starttime = t.time()
    ticker = str(ticker)
    artificialcrumb = CrumbCatcher(ticker)
    downloadurl = ("https://query1.finance.yahoo.com/v7/finance/download/" + ticker 
    + "?period1=-631123200&period2=1598374000&interval=1d&events=div&crumb=" + artificialcrumb)
    mainurl = "https://finance.yahoo.com/quote/" + ticker + "/history?p=" + ticker
    response = requests.post(downloadurl)#, data=CookieDict)
    datastr = response.text
    formatter = StringIO(datastr)
    df = pd.read_csv(formatter, sep = ',')
    df = df.set_index('Date')
    df.index = pd.to_datetime(df.index, format = "%Y/%m/%d") 
    for i in df.columns:
        df[i] =  pd.to_numeric(df[i], errors='coerce')
    endtime = t.time()
    duration = endtime - starttime 
    df = df.sort_index()
    return df
    # you may now write to file
    
    #df.to_csv(("F:\\Users\\AmatVictoriaCuram\\TemporaryCSV\\"+ ticker + ".csv"))
    
    #r = requests.get(mainurl)
    #BigCookie = r.headers['set-cookie']
    #BigCookieList = BigCookie.split(sep=';')
    #Cookie = r.cookies['B']
    #print(Cookie)
    #CookieDict = {'B' : Cookie}
    #web.open(url2, new = 2)