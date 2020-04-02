# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a formatting tool for adding carrots to index names 
#so they can be added to SymbolList for scraping/dataRequisition

#Import modules
import pandas as pd
#Read in text
data = pd.read_csv('Indicies.txt',  sep="\t",header = None,
                  names=['Ticker', 'EverythingElse'])
#Remove data
data = data.drop('EverythingElse', axis = 1)
#Text string
data['Carrot'] = '^'
#Add ^ to str
data['IndexTicker'] = data['Carrot'] + data['Ticker']
#Trim data 
data = data[1:]
#Drop carrot
data = data.drop(['Ticker','Carrot'], axis = 1)
#Iterable
ranger = range(0,len(data))
data['Index'] = ranger
#To dataframe
dataframe = pd.DataFrame(data, index = data['Index'])
dataframe = dataframe[1:].drop('Index', axis = 1)
#Display
print(dataframe)
#Save to file
dataframe.to_csv('IndexListo', sep = ',')
