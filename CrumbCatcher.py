# -*- coding: utf-8 -*-
"""

@author: @author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#If the Yahoo! response changes, it will be necessary to amend code
#This is a HTML scraping and formatting tool

#Define function
def CrumbCatcher(ticker):

    #Import modules
    import requests
    
    #Format ticker
    ticker = str(ticker)
    
    #Assign URL for post request
    url = 'http://finance.yahoo.com/quote/' + str(ticker)

    #Make post request
    page = requests.post(url)
    
    #Format response to text
    textI = page.text
    
    #Locate text in response
    markerI = textI.find('CrumbStore')
    #Assign trimmed response
    textII = textI[markerI:]

    #Locate text in trimmed response
    markerII = textII.find('StreamStore') - 3
    #Assign trimmed response
    textIII = textII[:markerII]

    #Locate text in trimmed response
    markerIII = textIII.rfind(':') + 1
    #Assign trimmed response
    textIV = textIII[markerIII:]
    
    #Format and reassign; remove "s
    textIV = textIV.replace('"','')
    
    #Return the crumb from URL
    return str(textIV)
