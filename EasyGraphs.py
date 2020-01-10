# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 20:24:43 2019

@author: AmatVictoriaCuramIII
"""

#Basic graphing tool for candlestick charts using matplotlib

#graphs
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from YahooGrabber import YahooGrabber
Asset = YahooGrabber('UVXY')
backup = YahooGrabber('UVXY')
Asset = Asset[-50:]
Asset['Date'] = Asset.index
AssetCopy = Asset[['Date', 'Open', 'High', 'Low','Close']].copy()
AssetCopy['Date'] = AssetCopy.index
AssetCopy['Date'] = AssetCopy['Date'].apply(mdates.date2num)
fig1, axe = plt.subplots(figsize = (10,5))
candlestick_ohlc(axe, AssetCopy.values, width=.6, colorup='green', colordown='red')
axe.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
