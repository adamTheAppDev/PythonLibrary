# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 19:50:19 2019

@author: AmatVictoriaCuramIII
"""

#This is a graphical display tool for candlestick charts + indicators
#It has a trading model inside, nice.

#Graphs
from YahooGrabber import YahooGrabber
from YahooSourceDailyGrabber import YahooSourceDailyGrabber
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
import numpy as np

#Acquire input data
string = 'STX'
Asset = YahooGrabber(string)
#Trimmer
Asset = Asset[-100:]
#Make column that represents X axis 
Asset['Index'] = Asset.index
#Format for mpl
Asset['IndexToNumber'] = Asset['Index'].apply(mdates.date2num)
#Format Dataframe to feed candlestick_ohlc()
AssetCopy = Asset[['IndexToNumber', 'Open', 'High', 'Low', 'Close', 'Adj Close']].copy()

#Create axe and define X and Y axis scale
figure, axe = plt.subplots(figsize = (10,5))
#Assign titles
plt.ylabel(string + ' Price')
plt.xlabel('Date') 

#Variable windows
#donchianwidow is used to find the min/max of the price range to make the long/short signal
#Smaller donchain window = more likely double days
donchianwindow = 55
#ATRwindow is used for volatility position sizing
ATRwindow = 20
#stopwindow is used for trailing high/low used for long/short exits
stopwindow = 13
#Counter tracks iteration progress
Counter = 0

#SubIndex column is a secondary index, it only exists to help identify exits
AssetCopy['SubIndex'] = range(0,len(AssetCopy))

#Log Returns
AssetCopy['LogRet'] = np.log(AssetCopy['Adj Close']/AssetCopy['Adj Close'].shift(1))
AssetCopy['LogRet'] = AssetCopy['LogRet'].fillna(0)

#ATR calculation using ATRwindow
AssetCopy['Method1'] = AssetCopy['High'] - AssetCopy['Low']
AssetCopy['Method2'] = abs((AssetCopy['High'] - AssetCopy['Close'].shift(1)))
AssetCopy['Method3'] = abs((AssetCopy['Low'] - AssetCopy['Close'].shift(1)))
AssetCopy['Method1'] = AssetCopy['Method1'].fillna(0)
AssetCopy['Method2'] = AssetCopy['Method2'].fillna(0)
AssetCopy['Method3'] = AssetCopy['Method3'].fillna(0)
AssetCopy['TrueRange'] = AssetCopy[['Method1','Method2','Method3']].max(axis = 1)
#ATR in points; not %
AssetCopy['ATR'] = AssetCopy['TrueRange'].rolling(window = ATRwindow,
                                center=False).mean()
#Market top and bottom calculation

#Technical calculations
#Donchian Channel
AssetCopy['RollingMax'] = AssetCopy['High'].rolling(20).max()
AssetCopy['RollingMin'] = AssetCopy['Low'].rolling(20).min()
#SMA
AssetCopy['SMA5'] = AssetCopy['Close'].rolling(5).mean()
AssetCopy['SMA20'] = AssetCopy['Close'].rolling(20).mean()
#N period ATR Setup
AssetCopy['Method1'] = AssetCopy['High'] - AssetCopy['Low']
AssetCopy['Method2'] = abs((AssetCopy['High'] - AssetCopy['Close'].shift(1)))
AssetCopy['Method3'] = abs((AssetCopy['Low'] - AssetCopy['Close'].shift(1)))
AssetCopy['Method1'] = AssetCopy['Method1'].fillna(0)
AssetCopy['Method2'] = AssetCopy['Method2'].fillna(0)
AssetCopy['Method3'] = AssetCopy['Method3'].fillna(0)
AssetCopy['TrueRange'] = AssetCopy[['Method1','Method2','Method3']].max(axis = 1)
AssetCopy['4wkATRPoints'] = AssetCopy['TrueRange'].rolling(window = 20, center=False).mean()        
AssetCopy['4wkATRPercent'] = AssetCopy['4wkATRPoints'] / AssetCopy['Close']
AssetCopy['ATRRollingMax'] = AssetCopy['4wkATRPercent'].rolling(20).max()
AssetCopy['ATRRollingMin'] = AssetCopy['4wkATRPercent'].rolling(20).min()
#Signal = Price </> min/max
#if price is greater than the max go long
AssetCopy['LongSignal'] = np.where(AssetCopy['High'] >= AssetCopy['RollingMax'].shift(1), 1, 0)
#if price is less than the min go short
AssetCopy['ShortSignal'] = np.where(AssetCopy['Low'] <= AssetCopy['RollingMin'].shift(1), 1, 0)

#If double signal days exist, then entry and P/L on those days will not be reflected correctly, spurious return stream
AssetCopy['DoubleDay'] = np.where(AssetCopy['LongSignal'] + AssetCopy['ShortSignal'] == 2, 1, 0)

#Next two lines combines long signal and short signal columns into a single column
#If there is a double day then a short entry is recorded
AssetCopy['Signal'] = np.where(AssetCopy['LongSignal'] == 1, 1, 0)
AssetCopy['Signal'] = np.where(AssetCopy['ShortSignal'] == 1, -1, AssetCopy['Signal'])

#if Rolling Min/Max is still being computed, stay out of market
AssetCopy['Signal'] = np.where(AssetCopy['RollingMax'] == np.nan, 0, AssetCopy['Signal'])

#Index values for segmenting data for trade analysis
SignalDates = list(AssetCopy['Signal'].loc[(AssetCopy['Signal'] != 0)].index)


#Trade ATR on signal day
AssetCopy['TradeATR'] = np.where(AssetCopy['Signal'] != 0, AssetCopy['ATR'].shift(1), np.nan)

#Exits other than initial 2 ATR stop, stopwindow is used here
#Asset1['LimitExitPrice'] = np.nan 
AssetCopy['ShortExitPrice'] =  AssetCopy['High'].rolling(window=stopwindow, center=False).max()
AssetCopy['LongExitPrice'] =  AssetCopy['Low'].rolling(window=stopwindow, center=False).min()


#Declare columns to record entry price and initial 2 ATR stop for unit one
AssetCopy['EntryPriceUnitOne'] = np.nan
AssetCopy['StopPriceUnitOne'] = np.nan

#Be sure to check for double signal days, gaps on first unit entry, and gaps on exits.

#Default stops and entries 
#Find the first trade of the signal period, so we can document entry prices
#Long entry first unit // enter one cent above previous high
AssetCopy['EntryPriceUnitOne'] = np.where(AssetCopy['Signal'] == 1, 
                              AssetCopy['RollingMax'].shift(1) + .01, np.nan)
#Short entry first unit // enter one cent below previous low
AssetCopy['EntryPriceUnitOne'] = np.where(AssetCopy['Signal'] == -1, 
              AssetCopy['RollingMin'].shift(1) - .01, AssetCopy['EntryPriceUnitOne'])

#Overlay
axe.plot(AssetCopy['IndexToNumber'], AssetCopy['RollingMax'], color = 'green', label = 'RollingMax')
axe.plot(AssetCopy['IndexToNumber'], AssetCopy['RollingMin'], color = 'red', label = 'RollingMin')
axe.plot(AssetCopy['IndexToNumber'], AssetCopy['SMA5'], color = 'black', label = 'SMA5')
axe.plot(AssetCopy['IndexToNumber'], AssetCopy['SMA20'], color = 'yellow', label = 'SMA20')
#Signal triangles..
axe.scatter(AssetCopy.loc[AssetCopy['LongSignal'] == 1, 'IndexToNumber'].values, AssetCopy.loc[AssetCopy['LongSignal'] == 1, 'EntryPriceUnitOne'].values, label='skitscat', color='green', s=50, marker="^")
axe.scatter(AssetCopy.loc[AssetCopy['ShortSignal'] == 1, 'IndexToNumber'].values, AssetCopy.loc[AssetCopy['ShortSignal'] == 1, 'EntryPriceUnitOne'].values, label='skitscat', color='red', s=50, marker="v")

#Plot the DF values with the figure, object
candlestick_ohlc(axe, AssetCopy.values, width=.6, colorup='green', colordown='red')
axe.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

#For ATR
figure2, axe2 = plt.subplots(figsize = (10,2))
plt.ylabel(string + ' ATR')
plt.xlabel('Date')
axe2.plot(AssetCopy['IndexToNumber'], AssetCopy['4wkATRPercent'], color = 'black', label = '4wkATRPercent')
axe2.plot(AssetCopy['IndexToNumber'], AssetCopy['ATRRollingMax'], color = 'green', label = 'ATRRollingMax')
axe2.plot(AssetCopy['IndexToNumber'], AssetCopy['ATRRollingMin'], color = 'red', label = 'ATRRollingMin')
axe2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
#Save image to CWD..
#plt.savefig('TestingTesting.png')
#Display figure
#plt.show()
