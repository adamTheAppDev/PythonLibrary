# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a technical analysis + database query tool

#Define function
def SCommodityChannelIndex(s):
    #Assign params
    constant = .02
    SMAwindow = 20
    #Calculate typical price
    s['TP'] = (s['High'] + s['Low'] + s['Adj Close']) / 3
    #Calculate SMA of typical price
    s['TPSMA'] = s['TP'].rolling(center=False, window = SMAwindow).mean()
    #Calculate standard deviation of TP
    s['MeanDeviation'] = s['TP'].rolling(center=False, window = SMAwindow).std()
    #Calculate commodity channel index
    s['CCI'] = ((s['TP'] - s['TPSMA'])/(constant*s['MeanDeviation']))
    #Output
    return s['CCI'][-1]
