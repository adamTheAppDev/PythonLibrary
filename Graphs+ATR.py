# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a graphical display tool

#Import modules
from YahooGrabber import YahooGrabber
from YahooSourceDailyGrabber import YahooSourceDailyGrabber
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates

#Assign ticker
string = 'STX'
#Request data
Asset = YahooGrabber(string)
#Trimmer
Asset = Asset[-150:]

#Make column that represents X axis 
Asset['Index'] = Asset.index
#Format for mpl
Asset['IndexToNumber'] = Asset['Index'].apply(mdates.date2num)
#Format Dataframe to feed candlestick_ohlc()
AssetCopy = Asset[['IndexToNumber', 'Open', 'High', 'Low','Close']].copy()
#X and Y axis scale
figure, axe = plt.subplots(figsize = (10,5))
#Assign titles
plt.ylabel(string + ' Price')
plt.xlabel('Date') 

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
#Overlay
axe.plot(AssetCopy['IndexToNumber'], AssetCopy['RollingMax'], color = 'green', label = 'RollingMax')
axe.plot(AssetCopy['IndexToNumber'], AssetCopy['RollingMin'], color = 'red', label = 'RollingMin')
axe.plot(AssetCopy['IndexToNumber'], AssetCopy['SMA5'], color = 'black', label = 'SMA5')
axe.plot(AssetCopy['IndexToNumber'], AssetCopy['SMA20'], color = 'yellow', label = 'SMA20')
#Plot the DF values with the figure, object 
candlestick_ohlc(axe, AssetCopy.values, width=.6, colorup='green', colordown='red')
axe.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

#For ATR
figure2, axe2 = plt.subplots(figsize = (10,2))
#Labels
plt.ylabel(string + ' ATR')
plt.xlabel('Date')
#ATR line graph and rolling min/max lines
axe2.plot(AssetCopy['IndexToNumber'], AssetCopy['4wkATRPercent'], color = 'black', label = '4wkATRPercent')
axe2.plot(AssetCopy['IndexToNumber'], AssetCopy['ATRRollingMax'], color = 'green', label = 'ATRRollingMax')
axe2.plot(AssetCopy['IndexToNumber'], AssetCopy['ATRRollingMin'], color = 'red', label = 'ATRRollingMin')
#Date formatting
axe2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
#Save image to CWD..
#plt.savefig('TestingTesting.png')
#Display figure
#plt.show()
