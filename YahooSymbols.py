# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is an outdated database query tool

#Import modules
import os 
import pandas as pd

#Iterable
index = range(0,len(os.listdir('Z:\\Users\\Username\\Database')))
#Read in tickers
goodsymbols = pd.DataFrame(os.listdir('Z:\\Users\\Username\\Database')
                           , columns = ['Symbol'])
#For all tickers
for i in index:
    #Add to dataframe
    goodsymbols['Symbol'][i] = goodsymbols['Symbol'][i]#[:-4]
#Confirmation
print(goodsymbols)
#Save to CSV
goodsymbols.to_csv('newgoodsymbols.csv',sep=',')
