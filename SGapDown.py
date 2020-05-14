# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a summary statistic + database query tool

#Define function
def SGapDown(s):
    #Percentage measure of how current high is lower than previous low
    s['GapDown'] = (s['Low'].shift(1) - s['High']) / s['Adj Close'].shift(1)
    #If positive, then current high is lower than previous low
    s['GapDown'] = s['GapDown'][s['GapDown'] > 0]
    s['GapDown'] = s['GapDown'].fillna(0)
    #Output
    return s['GapDown'].tail(1)
