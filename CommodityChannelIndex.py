# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a technical analysis tool

#Import modules
from YahooGrabber import YahooGrabber

#Assign variables
ticker = 'IWM'
constant = .02
SMAwindow = 20

s = YahooGrabber(ticker)

#Calculate typical price
s['TP'] = (s['High'] + s['Low'] + s['Adj Close']) / 3

#Calculate typical price simple moving average
s['TPSMA'] = s['TP'].rolling(center=False, window = SMAwindow).mean()

#Calculate average STDev
s['MeanDeviation'] = s['TP'].rolling(center=False, window = SMAwindow).std()

#Calculate commodity channel index
s['CCI'] = ((s['TP'] - s['TPSMA'])/(constant*s['MeanDeviation']))

#Top and bottom horizontal lines
s['Top'] = 100
s['Bottom'] = -100

#Trim data for indicator graph
s = s[SMAwindow:]

#Display
s[['CCI','Top','Bottom']].plot(grid = True, figsize = (8,3))
