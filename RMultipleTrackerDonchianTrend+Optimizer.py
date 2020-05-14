# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#Developed in Python 3.5 

#This is a trading strategy model with a brute force optimizer - under construction
#also see DonchianTrendEfficiencyFilterSingleStockSingleFrequency.py

#R Multiple Finder; Trade Data Tracking; Graphs

#Import modules
import numpy as np
#import random as rand
import pandas as pd
#import time as t
#from DatabaseGrabber import DatabaseGrabber
from YahooGrabber import YahooGrabber
#import matplotlib.pyplot as plt
import warnings 
import math
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
import random as rand
import time 

#Start timer
starttime = time.time()

#Assign ticker
Ticker1 = 'UVXY'
#Request data
Asset1 = YahooGrabber(Ticker1)

#Don't display warnings
warnings.filterwarnings("ignore", category = RuntimeWarning) 
pd.options.mode.chained_assignment = None 

#Declaration/Assignments
#Empty list
Empty = []
ParamsAndResultsList = []
#Empty dataframe
Trades = pd.DataFrame()
ParamsAndResults = pd.DataFrame()

#Number of iterations for optimizer
iterations = range(0,15) 
 
#Constraints in percentages; both unimplemented
Commission = .005
Slippage = .004

#Iteration tracking
Counter = 0

#SubIndex column is a secondary index, it exists to help identify exits
Asset1['SubIndex'] = range(0,len(Asset1))

#Calculate log Returns
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)

#ATR calculation using ATRwindow
Asset1['Method1'] = Asset1['High'] - Asset1['Low']
Asset1['Method2'] = abs((Asset1['High'] - Asset1['Close'].shift(1)))
Asset1['Method3'] = abs((Asset1['Low'] - Asset1['Close'].shift(1)))
Asset1['Method1'] = Asset1['Method1'].fillna(0)
Asset1['Method2'] = Asset1['Method2'].fillna(0)
Asset1['Method3'] = Asset1['Method3'].fillna(0)
Asset1['TrueRange'] = Asset1[['Method1','Method2','Method3']].max(axis = 1)

#Time series trimmer for in/out sample data
Asset1 = Asset1[-1250:] #In

#For number of iterations
for n in iterations:
    #Variable windows
    #Donchianwidow is used to find the min/max of the price range to make the long/short signal
    #Smaller donchain window = more likely double days
    donchianwindow = rand.randint(2,125)
    #ATRwindow is used for volatility position sizing
    ATRwindow = rand.randint(2,50)
    if ATRwindow >= donchianwindow:
        continue
    #Stopwindow is used for trailing high/low used for long/short exits
    stopwindow = rand.randint(2,100)
    #Number of ATR distance between stop
    numATR = rand.random() * 4

    #Define starting equity
    Equity = 100000000000
    #Risk for first trade
    RiskPerTrade = .005
    DollarRisk = Equity * RiskPerTrade

    #ATR in points; not %
    Asset1['ATR'] = Asset1['TrueRange'].rolling(window = ATRwindow,
                                center=False).mean()
    #Market top and bottom calculation
    Asset1['RollingMax'] = Asset1['High'].rolling(window=donchianwindow, center=False).max()
    Asset1['RollingMin'] = Asset1['Low'].rolling(window=donchianwindow, center=False).min()
    #Rolling stops
    Asset1['RollingLongStop'] = Asset1['Low'].rolling(window = stopwindow, center = False).min()
    Asset1['RollingShortStop'] = Asset1['High'].rolling(window = stopwindow, center = False).max()

    #Signal = Price </> min/max
    #If price is greater than the max go long
    Asset1['LongSignal'] = np.where(Asset1['High'] > Asset1['RollingMax'].shift(1), 1, 0)
    #If price is less than the min go short
    Asset1['ShortSignal'] = np.where(Asset1['Low'] < Asset1['RollingMin'].shift(1), 1, 0)

    #If double signal days exist, then entry and P/L on those days will not be reflected correctly, spurious return stream
    Asset1['DoubleDay'] = np.where(Asset1['LongSignal'] + Asset1['ShortSignal'] == 2, 1, 0)
    if sum(Asset1['DoubleDay']) > 0: 
        continue

    #Next two lines combines long signal and short signal columns into a single column
    #If there is a double day then a short entry is recorded
    Asset1['Signal'] = np.where(Asset1['LongSignal'] == 1, 1, 0)
    Asset1['Signal'] = np.where(Asset1['ShortSignal'] == 1, -1, Asset1['Signal'])

    #If Rolling Min/Max is still being computed, stay out of market
    Asset1['Signal'] = np.where(Asset1['RollingMax'] == np.nan, 0, Asset1['Signal'])

    #Index values for segmenting data for trade analysis
    SignalDates = list(Asset1['Signal'].loc[(Asset1['Signal'] != 0)].index)

    #Trade ATR on signal day
    Asset1['TradeATR'] = np.where(Asset1['Signal'] != 0, Asset1['ATR'].shift(1), np.nan)

    #Declare columns to record entry price and stop; assignment inside of while loop on per trade basis
    Asset1['EntryPriceUnitOne'] = np.nan
    Asset1['StopPriceUnitOne'] = np.nan

    #On the first signal we record entry, create stop regime, record  exit, record 
    #trade details, and then trim the time series to the next signal after exit. This process repeats.    
    #TradeSubset is a copy of Asset1 from the date of the first signal to the end of the time series
    TradeSubset = Asset1.loc[(Asset1.index >= SignalDates[0])] 

    #Every trade is in the while loop. If a position exists that is still open
    #at the end of the testing period, it is taken care of outside the while loop
    #while Counter < 1: #Use this instead of the while loop to go a certain number of trades into the iteration
    #While there is still a signal in the time series
    while sum(abs(TradeSubset['Signal'])) != 0:
        #Reset gap indicators
        GapEntry = 0
        GapExit = 0
        #Reset Entry and Exit Price
        EntryPrice = np.nan
        ExitPrice = np.nan
        #Signal dates
        IndexOfEntry = TradeSubset.index[0]
        #This is the ATR on the period before signal period
        TradeATR = Asset1['ATR'].shift(1).loc[Asset1.index == TradeSubset.index[0]][0]
        #Volatility position sizing based on nominal risk and market volatility; round down shares!!!
        #Does not account for slippage / market impact..
        numshares = (DollarRisk)/((TradeATR * numATR))//1
        #1 = long; -1 = short
        TradeDirection = TradeSubset['Signal'][0]
        #For long trades
        if TradeDirection == 1:
            #Establish non-gap entry price based on previous period rolling max
            EntryPrice = Asset1['RollingMax'].shift(1).loc[Asset1.index == TradeSubset.index[0]][0]
            #Check for entry gap; Open higher than previous period rolling max
            #If gap then buy on open
            if TradeSubset['Open'][0] > EntryPrice:
                #Enter on open
                EntryPrice = TradeSubset['Open'][0]
                #Record gap entry
                GapEntry = 1
            #Add slippage or market impact
            EntryPrice = EntryPrice # + .01
            #Assign to TradeSubset
            TradeSubset['EntryPriceUnitOne'][0] = EntryPrice
            #Calculate initial stop based on Direction and ATR
            TradeSubset['StopPriceUnitOne'][0] = EntryPrice - (numATR * TradeATR)
            #Forward fill stop 
            TradeSubset['StopPriceUnitOne'] = TradeSubset['StopPriceUnitOne'].ffill(
                                                        limit = (stopwindow - 1))
            #Add the trailing highest lows
            TradeSubset['StopPriceUnitOne'] = TradeSubset['StopPriceUnitOne'].fillna(TradeSubset['RollingLongStop'])
            #We want the cumulative maximum; thus preventing the stop from moving down.
            TradeSubset['StopPriceUnitOne'] = TradeSubset['StopPriceUnitOne'].cummax()
        
            #For every day the trade is open
            for r in range(len(TradeSubset['StopPriceUnitOne'])):
            #If low is lower than stop price
                if TradeSubset['Low'].iloc[r] < TradeSubset['StopPriceUnitOne'].shift(1).iloc[r]:
                #Record index of exit and get back to it                
                    IndexOfExit = TradeSubset.index[r]                
                    break          
            
            #Establish non-gap exit price based on previous period stop
            try:
                ExitPrice = TradeSubset['StopPriceUnitOne'].shift(1).loc[TradeSubset.index == IndexOfExit][0]
            #Except if there is an open trade then no IndexOfExit exists
            except IndexError:
                break
            #Check Open for exit gap through stop
            if TradeSubset['Open'].loc[IndexOfExit] < ExitPrice:
                #Record open price instead of stop price
                ExitPrice = TradeSubset['Open'].loc[IndexOfExit]
                #Record exit gap
                GapExit = 1
            #Calculate returns - slippage and commission go here.
            TradePercentReturn = (ExitPrice - EntryPrice) / ((RiskPerTrade ** -1) * DollarRisk)
            TradeDollarReturn = (ExitPrice - EntryPrice) * numshares
    
        #For short trades
        if TradeDirection == -1:
            #Establish non-gap entry price based on previous period rolling max
            EntryPrice = Asset1['RollingMin'].shift(1).loc[Asset1.index == TradeSubset.index[0]][0]
            #Check for entry gap; Open higher than previous period rolling max
            #If gap then buy on open
            if TradeSubset['Open'][0] < EntryPrice:
            #Record open price instead of stop price
                EntryPrice = TradeSubset['Open'][0]
            #Record gap entry
                GapEntry = 1
            #Add slippage or market impact
            EntryPrice = EntryPrice # - .01
            #Assign to TradeSubset
            TradeSubset['EntryPriceUnitOne'][0] = EntryPrice
            #Calculate initial stop based on Direction and ATR
            TradeSubset['StopPriceUnitOne'][0] = EntryPrice + (numATR * TradeATR)
            #Forward fill stop
            TradeSubset['StopPriceUnitOne'] = TradeSubset['StopPriceUnitOne'].ffill(
                                                        limit = (stopwindow - 1))
            #Add the trailing lowest highs
            TradeSubset['StopPriceUnitOne'] = TradeSubset['StopPriceUnitOne'].fillna(TradeSubset['RollingShortStop'])
            #We want the cumulative maximum; thus preventing the stop from moving down.
            TradeSubset['StopPriceUnitOne'] = TradeSubset['StopPriceUnitOne'].cummin()
        
            #For every day the trade is open
            for r in range(len(TradeSubset['StopPriceUnitOne'])):
            #If high is higher than stop price
                if TradeSubset['High'].iloc[r] > TradeSubset['StopPriceUnitOne'].shift(1).iloc[r]:
                #Record index of exit and get back to it                
                    IndexOfExit = TradeSubset.index[r]                
                    break          
            
            #Establish non-gap exit price based on previous period stop
            try:
                ExitPrice = TradeSubset['StopPriceUnitOne'].shift(1).loc[TradeSubset.index == IndexOfExit][0]
            except IndexError:
                break
            #Check Open for gap through stop
            if TradeSubset['Open'].loc[IndexOfExit] > ExitPrice:
            #Record open price instead of stop price
                ExitPrice = TradeSubset['Open'].loc[IndexOfExit]
            #Record gap exit            
                GapExit = 1
            TradePercentReturn = (EntryPrice - ExitPrice) / ((RiskPerTrade ** -1) * DollarRisk)
            TradeDollarReturn = (EntryPrice - ExitPrice) * numshares
        #If there is no exit signal, the trade is still open..    
        if math.isnan(ExitPrice) == True:
            break
        
        LengthOfTrade = TradeSubset['SubIndex'].loc[IndexOfExit] - TradeSubset['SubIndex'].loc[IndexOfEntry]
        #The SubIndex of the exit date is for continuing looking for rentry in new trade subset 
        SubIndexOfExit = TradeSubset['SubIndex'].loc[IndexOfExit]

        #R Multiple calculation, return based on initial risk
        RMultiple = TradeDollarReturn / DollarRisk

        #Log individual trade details in the Trade dataframe
        Empty.append(TradeDirection)
        Empty.append(IndexOfEntry)
        Empty.append(IndexOfExit)
        Empty.append(SubIndexOfExit)
        Empty.append(LengthOfTrade)
        Empty.append(GapEntry)
        Empty.append(GapExit)
        Empty.append(EntryPrice)
        Empty.append(ExitPrice)
        Empty.append(numshares)
        Empty.append(TradeATR)
        Empty.append(round(TradePercentReturn, 2))
        Empty.append(TradeDollarReturn)
        Empty.append(DollarRisk)
        Empty.append(RMultiple)
    
        #List to series
        Emptyseries = pd.Series(Empty)
        #Append series to Trades dataframe to log details
        Trades[Counter] = Emptyseries.values
        #Empty the list for next trade
        Empty[:] = [] 
        #Confirm trade number; Add to new column of Trade Dataframe
        Counter = Counter + 1
        #print(Counter) 
    
        #Recalculate equity and risk for next trade
        Equity = Equity + TradeDollarReturn
        DollarRisk = Equity * RiskPerTrade
        #This trimmer trims the above Trade out of the TradeSubset, then trims to the next signal day!
        TradeSubset = TradeSubset[(LengthOfTrade + 1):]
        SignalTrim = next((n for n, x in enumerate(TradeSubset['Signal']) if x), 0)
        TradeSubset = TradeSubset[SignalTrim:]
        #Reset stop price column
        TradeSubset['StopPriceUnitOne'] = np.nan
        
    #If there is a trade that is still open..
    if sum(abs(TradeSubset['Signal'])) != 0:
    #Reset gap indicators
        GapEntry = 0
        GapExit = 0
        #Reset Entry and Exit Price
        EntryPrice = np.nan
        ExitPrice = np.nan
        #Signal dates
        IndexOfEntry = TradeSubset.index[0]
        #This is the ATR on the period before signal period
        TradeATR = Asset1['ATR'].shift(1).loc[Asset1.index == TradeSubset.index[0]][0]
        #Volatility position sizing based on nominal risk and market volatility; round down shares!!!
        #Does not account for slippage / market impact..
        numshares = (DollarRisk)/((TradeATR * numATR))//1
        #1 = long; -1 = short
        TradeDirection = TradeSubset['Signal'][0]
        #For long trades
        if TradeDirection == 1:
            #Establish non-gap entry price based on previous period rolling max
            EntryPrice = Asset1['RollingMax'].shift(1).loc[Asset1.index == TradeSubset.index[0]][0]
            #Check for entry gap; Open higher than previous period rolling max
            #If gap then buy on open
            if TradeSubset['Open'][0] > EntryPrice:
            #Enter on open
                EntryPrice = TradeSubset['Open'][0]
            #Record gap entry
                GapEntry = 1
            #Add slippage or market impact
            EntryPrice = EntryPrice # + .01
            #Assign to TradeSubset
            TradeSubset['EntryPriceUnitOne'][0] = EntryPrice
            #Calculate initial stop based on Direction and ATR
            TradeSubset['StopPriceUnitOne'][0] = EntryPrice - (numATR * TradeATR)
            #Forward fill stop 
            TradeSubset['StopPriceUnitOne'] = TradeSubset['StopPriceUnitOne'].ffill(
                                                            limit = (stopwindow - 1))
            #Add the trailing highest lows
            TradeSubset['StopPriceUnitOne'] = TradeSubset['StopPriceUnitOne'].fillna(TradeSubset['RollingLongStop'])
            #We want the cumulative maximum; thus preventing the stop from moving down.
            TradeSubset['StopPriceUnitOne'] = TradeSubset['StopPriceUnitOne'].cummax()
            
            #For every day the trade is open
            for r in range(len(TradeSubset['StopPriceUnitOne'])):
                #If low is lower than stop price
                if TradeSubset['Low'].iloc[r] < TradeSubset['StopPriceUnitOne'].shift(1).iloc[r]:
                    #Record index of exit and get back to it                
                    IndexOfExit = TradeSubset.index[r]                
                    break          
                else:
                    IndexOfExit = TradeSubset.index[-1]
            #Calculate returns - slippage and commission go here    
            TradePercentReturn = (ExitPrice - EntryPrice) / ((RiskPerTrade ** -1) * DollarRisk)
            TradeDollarReturn = (ExitPrice - EntryPrice) * numshares
        
        #For short trades
        if TradeDirection == -1:
            #Establish non-gap entry price based on previous period rolling max
            EntryPrice = Asset1['RollingMin'].shift(1).loc[Asset1.index == TradeSubset.index[0]][0]
            #Check for entry gap; Open higher than previous period rolling max
            #If gap then buy on open
            if TradeSubset['Open'][0] < EntryPrice:
                #Record open price instead of stop price
                EntryPrice = TradeSubset['Open'][0]
                #Record gap entry
                GapEntry = 1
            #Add slippage or market impact
            EntryPrice = EntryPrice # - .01
            #Assign to TradeSubset
            TradeSubset['EntryPriceUnitOne'][0] = EntryPrice
            #Calculate initial stop based on Direction and ATR
            TradeSubset['StopPriceUnitOne'][0] = EntryPrice + (numATR * TradeATR)
            #Forward fill stop
            TradeSubset['StopPriceUnitOne'] = TradeSubset['StopPriceUnitOne'].ffill(
                                                            limit = (stopwindow - 1))
            #Add the trailing lowest highs
            TradeSubset['StopPriceUnitOne'] = TradeSubset['StopPriceUnitOne'].fillna(TradeSubset['RollingShortStop'])
            #We want the cumulative maximum; thus preventing the stop from moving down.
            TradeSubset['StopPriceUnitOne'] = TradeSubset['StopPriceUnitOne'].cummin()
            
            #For every day the trade is open
            for r in range(len(TradeSubset['StopPriceUnitOne'])):
                #If high is higher than stop price
                if TradeSubset['High'].iloc[r] > TradeSubset['StopPriceUnitOne'].shift(1).iloc[r]:
                    #Record index of exit and get back to it                
                    IndexOfExit = TradeSubset.index[r]                
                    break      
                else:
                    IndexOfExit = TradeSubset.index[-1]
    
            ExitPrice = TradeSubset['Adj Close'][-1]
            #Calculate returns - slippage and commission go here
            TradePercentReturn = (EntryPrice - ExitPrice) / ((RiskPerTrade ** -1) * DollarRisk)
            TradeDollarReturn = (EntryPrice - ExitPrice) * numshares
        #If there is no exit signal, the trade is still open..    
        if math.isnan(ExitPrice) == True:
                pass
            
        LengthOfTrade = TradeSubset['SubIndex'].loc[IndexOfExit] - TradeSubset['SubIndex'].loc[IndexOfEntry]
        #The SubIndex of the exit date is for continuing looking for rentry in new trade subset 
        SubIndexOfExit = TradeSubset['SubIndex'].loc[IndexOfExit]
    
        #R Multiple calculation, return based on initial risk
        RMultiple = TradeDollarReturn / DollarRisk
    
        #Log individual trade details in the Trade dataframe
        Empty.append(TradeDirection)
        Empty.append(IndexOfEntry)
        Empty.append(IndexOfExit)
        Empty.append(SubIndexOfExit)
        Empty.append(LengthOfTrade)
        Empty.append(GapEntry)
        Empty.append(GapExit)
        Empty.append(EntryPrice)
        Empty.append(ExitPrice)
        Empty.append(numshares)
        Empty.append(TradeATR)
        Empty.append(round(TradePercentReturn, 2))
        Empty.append(TradeDollarReturn)
        Empty.append(DollarRisk)
        Empty.append(RMultiple)
    
        #List to series
        Emptyseries = pd.Series(Empty)
        #Append series to Trades dataframe to log details
        Trades[Counter] = Emptyseries.values
        #Empty the list for next trade
        Empty[:] = [] 
        #Confirm trade number
        Counter = Counter + 1
        #print(Counter) 
        
        #Recalculate equity and risk for next trade
        Equity = Equity + TradeDollarReturn
        DollarRisk = Equity * RiskPerTrade
    
    #Last trade completed
    ParamsAndResultsList = [donchianwindow, ATRwindow, stopwindow, numATR, Equity, len(Trades.columns)] 
    #Add other stats

    ParamsAndResultsSeries = pd.Series(ParamsAndResultsList)
    ParamsAndResults[n] = ParamsAndResultsSeries.values
    #Display results
    print(Equity)

#Adjust row names for ParamsAndResults DataFrame    
ParamsAndResults = ParamsAndResults.rename(index={0: "donchianwindow", 1: "ATRwindow", 2: "stopwindow",
                                                  3: "numATR", 4:"Equity", 5:"numTrades"})

#Adjust row names for Trades DataFrame
Trades = Trades.rename(index={0: "TradeDirection", 1: "IndexOfEntry", 2: "IndexOfExit",
        3: "SubIndexOfExit", 4:"LengthOfTrade", 5: "GapEntry", 6: "GapExit", 7: "EntryPrice",
        8: "ExitPrice", 9: "numshares", 10: "TradeATR",
        11: "TradePercentReturn", 12: "TradeDollarReturn", 13:"DollarRisk", 
        14: "RMultiple"})
#End timer     
endtime = time.time()
#Timer stats
print("Processing took " + str(endtime - starttime) + " seconds.")
