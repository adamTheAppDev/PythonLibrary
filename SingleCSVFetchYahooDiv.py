# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is an HTML scraper + I/O + formatting tool

#Import module
import requests
from io import StringIO
import pandas as pd
import time as t
from CrumbCatcher import CrumbCatcher

#Start timer
starttime = t.time()
#Assign ticker
ticker = "A"
#Get crumb
artificialcrumb = str(CrumbCatcher())
#Assign download URL
downloadurl = ("https://query1.finance.yahoo.com/v7/finance/download/" + ticker 
+ "?period1=-631123200&period2=1598374000&interval=1d&events=div&crumb=" + artificialcrumb)
#Post request
response = requests.post(downloadurl)#, data=CookieDict)
#Format response
datastr = response.text
formatter = StringIO(datastr)
#Assign to dataframe
df = pd.read_csv(formatter, sep = ',')
#Set index
df = df.set_index('Date')
#Format index
df.index = pd.to_datetime(df.index, format = "%Y/%m/%d") 
#End timer
endtime = t.time()
#Timer stats
duration = endtime - starttime 

#Write to file
df.to_csv(("F:\\Users\\Username\\DirectoryLocation\\"+ ticker + "div.csv"))
