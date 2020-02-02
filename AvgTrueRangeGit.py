"""
Spyder Editor
"""

#This is a technical analysis tool

#Import modules
from YahooGrabber import YahooGrabber
import numpy as np

#Input ticker
ticker = 'SPY'
#Data request
s = YahooGrabber(ticker)

#Variable assignment
window = 14

#ATR calculation
s['Method1'] = s['High'] - s['Low']
s['Method2'] = abs((s['High'] - s['Close'].shift(1)))
s['Method3'] = abs((s['Low'] - s['Close'].shift(1)))
s['Method1'] = s['Method1'].fillna(0)
s['Method2'] = s['Method2'].fillna(0)
s['Method3'] = s['Method3'].fillna(0)
s['TrueRange'] = s[['Method1','Method2','Method3']].max(axis = 1)
s['AverageTrueRange'] = s['TrueRange'].rolling(window = window,
                                center=False).mean
#Trim out the window period for graph
trim = (window * 2 - 1)
s = s[trim:]

#Graphical display
s[['AverageTrueRange']].plot(grid=True, figsize=(8,3))
