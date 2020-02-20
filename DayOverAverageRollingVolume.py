# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a summary statistic tool

def DayOverAverageRollingVolume(s):
    window = 60
    s['AverageRollingVolume'] = s['Volume'].rolling(center=False, 
                                                        window=window).mean()
    s['DayOverARV'] = s['Volume']/s['AverageRollingVolume'] 
    return s['DayOverARV'].tail(1)
