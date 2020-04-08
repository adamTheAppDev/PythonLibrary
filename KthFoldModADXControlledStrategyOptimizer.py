# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a brute force optimization tool that is part of a kth fold optimization tool

#Define function
def DefModADXControlledStrategyOptimizer(ranger2, s):
    #Import modules
    import numpy as np
    import pandas as pd
    import random as rand
    #Assign empty structures
    empty = []
    winners = pd.DataFrame()
    #For total iterations passed in as param
    for r in ranger: 
        #Random variable assignment
        a = rand.randint(2,15)
        b = rand.randint(2,15)
        c = rand.random() * 3
        d = rand.random() * 3
        e = rand.random() * 3
        f = rand.random() * 3
        #Calculate log returns
        s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
        s['LogRet'] = s['LogRet'].fillna(0)
        #Directional metodology
        s['Regime'] = np.where(s['Advice'] > -1.874201, 1, 0)
        s['Regime'] = np.where(s['Advice'] < -.328022, -1, s['Regime'])
        #Apply position to returns 
        s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
        s['Strategy'] = s['Strategy'].fillna(0)
        s['NewStrategy'] = s['Strategy']
        
        #Candle width in %
        s['Width'] = (s['High'] - s['Low'])/s['Open'] 
        #Over night volatility
        s['OverNight'] = (s['Open'] - s['Adj Close'].shift(1))/s['Adj Close'].shift(1)
        #Rolling average market volatility
        s['RollingWidth'] = s['Width'].rolling(center = False, window=a).mean()
        s['RollingOverNight'] = abs(s['OverNight']).rolling(center=False, window=b).mean()
        #Up days
        s['DayUp'] = (s['High'] - s['Adj Close'].shift(1))/s['Open']
        s['DayUp'] = s['DayUp'][s['DayUp']> 0]
        s['DayUp'] = s['DayUp'].fillna(0)
        #Down days
        s['DayDown'] = (s['Adj Close'].shift(1) - s['Low'])/s['Open']
        s['DayDown'] = s['DayDown'][s['DayDown']> 0]
        s['DayDown'] = s['DayDown'].fillna(0)
        #Performance metrics
        s['sharpe'] = (s['Strategy'].mean()-abs(s['LogRet'].mean()))/s['Strategy'].std()
        #If up day then width divided by factor
        s['LongGains'] = np.where(s['DayUp'] >= (s['RollingWidth']/c),s['RollingWidth']/c,0)
        #If down day then width divided by factor
        s['ShortGains'] = np.where(s['DayDown'] >= (s['RollingWidth']/d),s['RollingWidth']/d,0)
        #Regime change signals
        s['LongStop'] = np.where(s['OverNight'] <= (s['RollingWidth'].shift(1)/e * -1),
                                                        s['OverNight'] ,0)
        s['ShortStop'] = np.where(s['OverNight'] >= s['RollingWidth'].shift(1)/f,
                                                        (s['OverNight']*-1) ,0)
        #New regime
        s['NewStrategy'] = np.where(s['Regime'].shift(1) == 1,s['LongGains'],0)
        s['NewStrategy'] = np.where(s['Regime'].shift(1) == -1,s['ShortGains'],s['NewStrategy'])
        s['NewStrategy'] = np.where(s['NewStrategy'] == 0, s['Strategy'], s['NewStrategy'])
        s['NewStrategy'] = np.where(s['LongStop'] < 0, s['LongStop'], s['NewStrategy'])
        s['NewStrategy'] = np.where(s['ShortStop'] < 0, s['ShortStop'], s['NewStrategy'])
        #New performance metric
        s['newsharpe'] = (s['NewStrategy'].mean()-abs(s['LogRet'].mean()))/s['NewStrategy'].std()  
        #Constraints
        if s['newsharpe'][-1] < -400:
            continue
        #Add params and metrics to list 
        empty.append(a)
        empty.append(b)
        empty.append(c)
        empty.append(d)
        empty.append(e)
        empty.append(f)
        empty.append(s['sharpe'][-1])
        empty.append(s['newsharpe'][-1])    
        #List to Series
        emptyseries = pd.Series(empty)
        #Series to dataframe
        winners[r] = emptyseries.values
        #Clear list
        empty[:] = [] 
    #Metric of choice
    z = winners.iloc[7]
    #Threshold
    w = np.percentile(z, 80)
    v = [] #this variable stores the Nth percentile of top params
    DS1W = pd.DataFrame() #this variable stores your params for specific dataset
    #For all params
    for h in z:
        #If greater than threshold
        if h > w:
            #Add to list
          v.append(h)
    #For all top params
    for j in v:
          #Get column number of param
          r = winners.columns[(winners == j).iloc[7]]    
          #Add param sets to dataframe by column number
          DS1W = pd.concat([DS1W,winners[r]], axis = 1)
    #Top metric
    y = max(z)
    #This is the column number of top param
    x = winners.columns[(winners == y).iloc[7]] 
    #Output top param/metric set
    return winners[x] 
        
