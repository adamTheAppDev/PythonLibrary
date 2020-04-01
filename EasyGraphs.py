# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#Basic graphing tool for candlestick charts using matplotlib

#Import modules
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from YahooGrabber import YahooGrabber

#Request data
Asset = YahooGrabber('UVXY')
backup = YahooGrabber('UVXY')
#Trim time series
Asset = Asset[-50:]
#Add date index
Asset['Date'] = Asset.index
#Copy for candlesticks
AssetCopy = Asset[['Date', 'Open', 'High', 'Low','Close']].copy()
#Add date index
AssetCopy['Date'] = AssetCopy.index
#Date formatting
AssetCopy['Date'] = AssetCopy['Date'].apply(mdates.date2num)
#Graph object
fig1, axe = plt.subplots(figsize = (10,5))
#Graph candlestick object
candlestick_ohlc(axe, AssetCopy.values, width=.6, colorup='green', colordown='red')
#Date formatting
axe.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
