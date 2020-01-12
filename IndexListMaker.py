# -*- coding: utf-8 -*-
"""
Created on Fri May 19 14:02:48 2017

@author: AmatVictoriaCuramIII
"""

#This is a formatting tool for adding carrots to index names 
#so they can be added to SymbolList for scraping/dataRequisition

import pandas as pd 
data = pd.read_csv('Indicies.txt',  sep="\t",header = None,
                  names=['Ticker', 'EverythingElse'])
data = data.drop('EverythingElse', axis = 1)
data['Carrot'] = '^'
data['IndexTicker'] = data['Carrot'] + data['Ticker']
data = data[1:]
data = data.drop(['Ticker','Carrot'], axis = 1)
ranger = range(0,len(data))
data['Index'] = ranger
dataframe = pd.DataFrame(data, index = data['Index'])
dataframe = dataframe[1:].drop('Index', axis = 1)
print(dataframe)
dataframe.to_csv('IndexListo', sep = ',')
