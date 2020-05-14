# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a summary statistic + database query tool

#Define function
def SAverageRollingVolume(s):
    #Calculate average rolling volume
    s['AverageRollingVolume'] = s['Volume'].rolling(center=False, 
                                                        window=252).mean()
    #Output
    return s['AverageRollingVolume'].tail(1)
