# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 15:25:03 2020

@author: AmatVictoriaCuramIII
"""

#Import modules
import requests
import pandas as pd
import time as t
import json

#from CrumbCatcherII import CrumbCatcherII

#Start timer
starttime = t.time()

#Ticker formatting
ticker = str('^GSPC')

#Variable assignment
Asset = pd.DataFrame()
#Assign URL for post request
url = ('http://finance.yahoo.com/quote/' + ticker + '/history?period1=1552017587' +
       '&period2=1552397400&interval=1d&filter=history&frequency=1d')
print('URL = ' + url)
#Make post request
page = requests.post(url)
print(page)
#Format response to text
textI = page.text

#Locate text in response
markerI = textI.find('[{"date":')
#Assign trimmed response
textI = textI[markerI:]

#Locate text in trimmed response
markerII = textI.find(',"isPending":false')
#Assign trimmed response
textI = textI[:markerII]
#text to json
textI = json.loads(textI)

for i in textI:
    Asset = Asset.append(i, ignore_index = True)
    
#Rename columns
Asset = Asset.rename(columns={"adjclose": "Adj Close", "close": "Close", "date": "Date", 
                   "high": "High", "low": "Low", "open": "Open", "volume": "Volume"})    
    
#Format datetime index
Asset['Date'] = pd.to_datetime(Asset['Date'], unit = 's')
Asset['Date'] = Asset['Date'].dt.date

#Set index to Date
Asset = Asset.set_index('Date')

#End timer    
endtime = t.time()
#Time calculation
duration = endtime - starttime
#Display time taken for request and formatting
print("Data request for " + ticker + " took " + str(duration) +" seconds.") 