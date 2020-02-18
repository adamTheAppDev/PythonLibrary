# -*- coding: utf-8 -*-
"""
Created on Wed May  3 15:14:55 2017

@author: AmatVictoriaCuramIII
"""

#This is a HTML parsing/scraping tool

#Define function
def CrumbCatcher():
    #Import modules
    import requests
    
    #URL for scraping
    page = requests.post('http://finance.yahoo.com/quote/SPY')
    #POST request to text
    textfile = page.text
    #Locate text
    num = textfile.find('CrumbStore')
    #Trim at location
    textfile2 = textfile[num:]
    #Locate text
    num2 = textfile2.find('QuotePageStore') - 3
    #Trim at location
    textfile3 = textfile2[:num2]
    #Locate text
    num3 = textfile3.rfind(':') + 1
    #Trim at location
    textfile4 = textfile3[num3:]
    #Clean up "s
    textfile4.replace('"','')
    #Output
    return textfile4
