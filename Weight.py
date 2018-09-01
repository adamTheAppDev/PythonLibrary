# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 11:27:35 2017

@author: AmatVictoriaCuramIII
"""
#Get modules
#import scipy as sp
import numpy as np
from pandas_datareader import data
import pandas as pd
#portfolio set up
port = ['^GSPC', '^RUA']
numsec = len(port)
equalweight = 1/numsec
df2 = pd.DataFrame(columns=[])
x=0
y=0
#HERE'S AN IDEA print(list(enumerate(port, start=1)))
#List the log returns in columns 
for s in port:
    x = x + 1
    y = y - 1
    s = data.DataReader(s, 'yahoo', start='1/1/1900', end='01/01/2050') 
    s[x] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) #log returns
    s['equalweight'] = equalweight
    s[y] = s[x] * s['equalweight'] #This is the weighted return
    df2 = pd.concat([df2,s[x],s[y]], axis=1)
#Multiply the individual columns by the last and sum
#df2['portfolioreturn'] = df2[(range(-1, -numsec, -1))]
df2 = pd.concat([df2,s['equalweight']], axis=1)
print(df2)