# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a summary statistic tool

#Define function
def DayOverAverageRollingVolume(s):
    #Variable assignment
    window = 60
    #Rolling volume calculation
    s['AverageRollingVolume'] = s['Volume'].rolling(center=False, 
                                                        window=window).mean()
    #Relative volume calculation
    s['DayOverARV'] = s['Volume']/s['AverageRollingVolume'] 
    #Output summary statistic
    return s['DayOverARV'].tail(1)
