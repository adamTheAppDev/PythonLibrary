# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a weighting tester for two asset portfolio analysis

#Import modules
#import scipy as sp
import numpy as np
from pandas_datareader import data
import pandas as pd

#Assign tickers
port = ['^GSPC', '^RUA']
#Number of tickers
numsec = len(port)
#Split to equal sizes
equalweight = 1/numsec
#Create dataframe
df2 = pd.DataFrame(columns=[])
#Variable assignment
x=0
y=0
#Alternative method
#print(list(enumerate(port, start=1)))
#List the log returns in columns 
for s in port:
    #Increment
    x = x + 1
    y = y - 1
    #Request data
    s = data.DataReader(s, 'yahoo', start='1/1/1900', end='01/01/2050') 
    #Calculate log returns
    s[x] = np.log(s['Adj Close']/s['Adj Close'].shift(1))
    #Position sizing
    s['equalweight'] = equalweight
    #Weighted return
    s[y] = s[x] * s['equalweight'] 
    #Add to dataframe
    df2 = pd.concat([df2,s[x],s[y]], axis=1)
#Multiply the individual columns by the last and sum
#df2['portfolioreturn'] = df2[(range(-1, -numsec, -1))]
#Add weights to dataframe
df2 = pd.concat([df2,s['equalweight']], axis=1)
#Display results
print(df2)
