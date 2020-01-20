# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a HTML scraper, I/O, and formatting tool that requests OHLC data from Yahoo!

#Define function
def YahooGrabber(ticker):

    #Import modules
    import requests
    from io import StringIO
    import pandas as pd
    import time as t
    from CrumbCatcher import CrumbCatcher

    #Start timer
    starttime = t.time()

    #Ticker formatting
    ticker = str(ticker)

    #Get crumb for URL validation/confirmation
    artificialcrumb = CrumbCatcher(ticker)

    #Assign URL for use in post request
    downloadurl = ("https://query1.finance.yahoo.com/v7/finance/download/" + ticker 
    + "?period1=-631123200&period2=1598374000&interval=1d&events=history&crumb=" + artificialcrumb)

    #Make post request
    response = requests.post(downloadurl)#, data=CookieDict)

    #Format reposonse
    datastr = response.text
    formatter = StringIO(datastr)

    #Reformat into DataFrame object
    df = pd.read_csv(formatter, sep = ',')
    #Set index to Date
    df = df.set_index('Date')
    #Format datetime index
    df.index = pd.to_datetime(df.index, format = "%Y/%m/%d") 

    #Change data type of all values in table to numbers    
    for i in df.columns:
        df[i] =  pd.to_numeric(df[i], errors='coerce')    

    #Optional write to file as CSV or pickle 
    #See YahooSource.py for Database Creation + Management
    #df.to_csv(("F:\\Users\\ComputerName\\DatabaseFolder\\"+ ticker + ".csv"))
    #df.to_pickle(df, ("F:\\Users\\ComputerName\\DatabaseFolder\\"+ ticker))

    #End timer    
    endtime = t.time()
    #Time calculation
    duration = endtime - starttime
    #Display time taken for request and formatting
    print("Data request took " + str(duration) +" seconds.") 

    return df
