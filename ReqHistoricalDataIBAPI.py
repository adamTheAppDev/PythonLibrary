# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#Brian from stackoverflow hooked it up with the framework for this one
#Slight modifications to upgrade functionality

#Import modules
from time import sleep, strftime
from ib.ext.Contract import Contract
from ib.opt import ibConnection, message
import pandas as pd
import numpy as np
import time
#import math 

#Variable assignment

#RangeID = range(1,33)
#RangeArray = np.array(RangeID)
UniverseCSVList = pd.read_pickle('F:\\Users\\AmatVictoriaCuram\\FDL\\'+
                      'DataSources\\NASDAQSource\\UniverseLists\\Universe2018')
UniverseList =  [s[:-4] for s in UniverseCSVList]
#UniverseList = UniverseList[:35]
#TotalConnections = len(UniverseList)
#NumTiles = math.ceil(TotalConnections/32)
#ConnectionIDs = np.tile(RangeArray, NumTiles)
#ConnectionIDs = ConnectionIDs[:len(UniverseList)]
#for t in (UniverseList):
def nextValidId_handler(msg):
    print(msg)
    inner()

hist = []
ticker = str()


def hist_data_handler(msg):
    print(msg)
    if "finished" in msg.date:
        print('disconnecting', con.disconnect())
        df = pd.DataFrame(index=np.arange(0, len(hist)), columns=('Date', 'Open', 'High', 'Low', 'Close'))
        for index, msg in enumerate(hist):
            df.loc[index,'Date':'Close'] = msg.date, msg.open, msg.high, msg.low, msg.close
        #Set index to Date
        df = df.set_index('Date')
       #Format datetime index
        df.index = pd.to_datetime(df.index, format = "%Y/%m/%d") 
        #Optional save to CSV functionality
        df.to_csv(("C:\\Users\\AmatVictoriaCuramIII\\Desktop\\" + globals()[ticker] + ".csv"))
        print(df)
    else:
        hist.append(msg)    

def error_handler(msg):
    print(msg)

if __name__ == '__main__':

    con = ibConnection(port=7497,clientId=1)
    con.register(error_handler, message.Error)
    con.register(nextValidId_handler, message.nextValidId)
    con.register(hist_data_handler, message.historicalData)
    con.connect()

    print(con.isConnected())

    def inner():

        CntrctObj = Contract()
        CntrctObj.m_secType = "STK" 
        CntrctObj.m_symbol = "AAPL"
        #globals()[ticker] = CntrctObj.m_symbol         
        CntrctObj.m_currency = "USD"
        CntrctObj.m_exchange = "SMART"
        endtime = strftime('%Y%m%d %H:%M:%S')
        print(endtime)
        con.reqHistoricalData(1, CntrctObj, endtime, "1 Y", "1 day", "MIDPOINT", 1, 2)

    print(con.isConnected())
#time.sleep(.5)
        
