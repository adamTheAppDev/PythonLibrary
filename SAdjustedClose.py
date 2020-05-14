# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a database query tool
#Define function
def SAdjustedClose(s):
    #Output
    return s['Adj Close'].tail(1)
