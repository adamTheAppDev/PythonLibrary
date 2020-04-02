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
string = 'X'
#Request data
Asset = YahooGrabber(string)
#Trimmer
Asset = Asset[-50:]1

#Make column that represents X axis 
Asset['Index'] = Asset.index
#Format for mpl
Asset['IndexToNumber'] = Asset['Index'].apply(mdates.date2num)
#Format Dataframe to feed candlestick_ohlc()
AssetCopy = Asset[['IndexToNumber', 'Open', 'High', 'Low','Close']].copy()
#X and Y axis scale
figure, axe = plt.subplots(figsize = (10,5))
#Assign titles
plt.ylabel(string)
plt.xlabel('Date') 

#Technical calculations
#Donchian Channel
AssetCopy['RollingMax'] = AssetCopy['High'].rolling(20).max()
AssetCopy['RollingMin'] = AssetCopy['Low'].rolling(20).min()
#SMA
#AssetCopy['SMA5'] = AssetCopy['Close'].rolling(5).mean()
#AssetCopy['SMA20'] = AssetCopy['Close'].rolling(20).mean()

#Overlay
axe.plot(AssetCopy['IndexToNumber'], AssetCopy['RollingMax'], color = 'green', label = 'RollingMax')
axe.plot(AssetCopy['IndexToNumber'], AssetCopy['RollingMin'], color = 'red', label = 'RollingMin')
#axe.plot(AssetCopy['IndexToNumber'], AssetCopy['SMA5'], color = 'black', label = 'SMA5')
#axe.plot(AssetCopy['IndexToNumber'], AssetCopy['SMA20'], color = 'yellow', label = 'SMA20')

#Plot the DF values with the figure, object 
candlestick_ohlc(axe, AssetCopy.values, width=.6, colorup='green', colordown='red')
#Date formatting
axe.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

#Save image to CWD..
#plt.savefig('TestingTesting.png')
#Display figure
#plt.show()
