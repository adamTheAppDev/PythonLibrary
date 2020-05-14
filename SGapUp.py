# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a summary statistic + database query tool

#Define function
def SGapUp(s):
    #Import modules
    import numpy as np
    #Percentage measure of how much higher current low is above previous high
    s['GapUp'] = (s['High'].shift(1) - s['Low']) / s['Adj Close'].shift(1)
    #If negative, then current low is above previous high
    s['GapUp'] = s['GapUp'][s['GapUp'] < 0]
    s['GapUp'] = s['GapUp'].fillna(0)
    #Make negative results positive
    s['GapUp'] = np.where(s['GapUp'] == 0 , 0, (-1*s['GapUp']))
    #Output
    return s['GapUp'].tail(1)    
