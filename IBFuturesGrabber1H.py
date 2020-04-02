# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#Import modules
from time import strftime
from ib.ext.Contract import Contract
from ib.opt import ibConnection, message
import pandas as pd
import numpy as np
#import time
#import math 

#Variable assignment
#Iterable connection number for tile
#RangeID = range(1,33)
#To array
#RangeArray = np.array(RangeID)
#Get tickers
#UniverseCSVList = pd.read_pickle('F:\\Users\\AmatVictoriaCuram\\FDL\\'+
#                      'DataSources\\NASDAQSource\\UniverseLists\\Universe2018')
#Trim extensions
#UniverseList =  [s[:-4] for s in UniverseCSVList]
#Trim for sampling/testing
#UniverseList = UniverseList[:35]
#TotalConnections = len(UniverseList)
#IB can only accept 32 connections
#NumTiles = math.ceil(TotalConnections/32)
#Make range
#ConnectionIDs = np.tile(RangeArray, NumTiles)
#Trim tange
#ConnectionIDs = ConnectionIDs[:len(UniverseList)]
#For each ticker in list
#for t in (UniverseList):
#Define function
def nextValidId_handler(msg):
    #Message from API
    print(msg)
    #Inner function
    inner()
#Data structures
hist = []
ticker = str()

#Define function
def my_hist_data_handler(msg):
    #Message from API
    print(msg)
    #If queue empty
    if "finished" in msg.date:
        #Call to disconnect
        print('disconnecting', con.disconnect())
        #Candle data
        df = pd.DataFrame(index=np.arange(0, len(hist)), columns=('Date', 'Open', 'High', 'Low', 'Close'))
        #Add data to dataframe
        for index, msg in enumerate(hist):
            df.loc[index,'Date':'Close'] = msg.date, msg.open, msg.high, msg.low, msg.close
        #Set index to Date
        df = df.set_index('Date')
        #Format datetime index
        df.index = pd.to_datetime(df.index, unit = 's')
        #Convert float to float64
        for i in df.columns:
            df[i] =  pd.to_numeric(df[i], errors='coerce')
        #Save to pickle
        pd.to_pickle(df, "F:\\Users\\AmatVictoriaCuram\\FDL\\DataSources\\IBSource\\DataName")
        print(df)
    else:
        #'finished' not in msg
        hist.append(msg)    

#Define function to handle API errors
def error_handler(msg):
    print(msg)

    #Run
if __name__ == '__main__':
    #Connection object
    con = ibConnection(port=7497,clientId=1)
    #Add functions
    con.register(error_handler, message.Error)
    con.register(nextValidId_handler, message.nextValidId)
    con.register(my_hist_data_handler, message.historicalData)
    #Call to connect
    con.connect()
    #Confirm connection
    print(con.isConnected())
    #Define inner function
    def inner():
        #Create contract object
        CntrctObj = Contract()
        CntrctObj.m_secType = "FUT" 
        CntrctObj.m_symbol = "ES"
        #Custom symbol field
        globals()[ticker] = CntrctObj.m_symbol         
        CntrctObj.m_currency = "USD"
        CntrctObj.m_exchange = "GLOBEX"
        CntrctObj.m_localSymbol = "ESH0"
        #Date formatting based on frequency
        endtime = strftime('%Y%m%d %H:%M:%S')
        #Confirm
        print(endtime)
        #Request historical data
        con.reqHistoricalData(1, CntrctObj, endtime, "1 Y", "1 hour", "MIDPOINT", 1, 2)
    #Confirm connection
    print(con.isConnected())
#Pause for disconnect
#time.sleep(.5)
        
