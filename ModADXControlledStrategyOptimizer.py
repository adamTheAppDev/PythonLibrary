# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is part of a kth fold optimization tool
#pandas_datareader is deprecated, use YahooGrabber

#Import modules
from DefModADXControlledStrategyOptimizer import DefModADXControlledStrategyOptimizer
import numpy as np
import pandas as pd
import random as rand
#from pandas_datareader import data

#Assign ticker / variable assignment
ticker = '^RUT'
multiplier = 400
ranger1 = range(0,multiplier)
iterations = 5000
ranger2 = range(0,iterations) #Pass ranger
#Empty data structures
empty = []
counter = 0
dataset = pd.DataFrame()

#Read in data
Aggregate = pd.read_pickle('RUTModADXAGGSHARPE065')
Aggregate = Aggregate.loc[:,~Aggregate.columns.duplicated()]
#s = data.DataReader(ticker, 'yahoo', start='04/01/2017', end='01/01/2050') 
s = pd.read_pickle('RUTModADXAGGAdvice07_50') # this is just for testing with a graph

#For number of iterations
for r in ranger1:
    #Iteration trackking
    print(counter)
    counter = counter + 1
    #Get optimal params
    DSW = DefModADXControlledStrategyOptimizer(ranger2, s)
    #Add params to dataset
    dataset = pd.concat([dataset,DSW], axis = 1)
#Metric of choice
zz = dataset.iloc[7]
#Top metric
yy = max(zz)
#Find column ID of top param set
xx = dataset.columns[(dataset == yy).iloc[7]]
#Display top param set
print(dataset[xx])
