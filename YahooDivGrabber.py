# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is an HTML scraper + I/O + formatting tool 

#Define function
def YahooDivGrabber(ticker):
    #Import modules
    import requests
    from io import StringIO
    import pandas as pd
    import time as t
    from CrumbCatcher import CrumbCatcher
    #Start timer
    starttime = t.time()
    #Assign ticker
    ticker = str(ticker)
    #Get crumb
    artificialcrumb = CrumbCatcher(ticker)
    #Assign download URL
    downloadurl = ("https://query1.finance.yahoo.com/v7/finance/download/" + ticker 
    + "?period1=-631123200&period2=1598374000&interval=1d&events=div&crumb=" + artificialcrumb)
    mainurl = "https://finance.yahoo.com/quote/" + ticker + "/history?p=" + ticker
    #Post request
    response = requests.post(downloadurl)#, data=CookieDict)
    #Format response
    datastr = response.text
    formatter = StringIO(datastr)
    #Read in data
    df = pd.read_csv(formatter, sep = ',')
    #Set index
    df = df.set_index('Date')
    #Format index
    df.index = pd.to_datetime(df.index, format = "%Y/%m/%d") 
    #Make columns numeric
    for i in df.columns:
        df[i] =  pd.to_numeric(df[i], errors='coerce')
    #End timer    
    endtime = t.time()
    #Timer stats
    duration = endtime - starttime 
    #Sort by date
    df = df.sort_index()
    #Output
    return df
    #Write to file
    #df.to_csv(("Z:\\Users\\Username\\DirectoryLocation\\"+ ticker + ".csv"))
