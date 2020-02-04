# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a technical analysis tool

#Import modules
from YahooGrabber import YahooGrabber

#Input ticker
ticker = '^GSPC'

#Request data
s = YahooGrabber(ticker)

#Assign variable
window = 20

#Rolling SMA + STD calculation
s['nDaySMA'] = s['Adj Close'].rolling(window=window, center=False).mean()
s['nDaySTD'] = s['Adj Close'].rolling(window=window, center=False).std()

#Bollinger band calculation
s['UpperBand'] = s['nDaySMA'] + (s['nDaySTD'] * 2)
s['LowerBand'] = s['nDaySMA'] - (s['nDaySTD'] * 2)
s['BandWidth'] = ((s['UpperBand'] - s['LowerBand'])/s['nDaySMA'])*100

#Trim data
s = s[window:]

#Indicator graph
s['BandWidth'].plot(grid=True, figsize=(8, 3))
