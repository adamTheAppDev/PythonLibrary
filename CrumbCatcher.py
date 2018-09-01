# -*- coding: utf-8 -*-
"""
Created on Wed May  3 15:14:55 2017

@author: AmatVictoriaCuramIII
"""
def CrumbCatcher():

    import requests 
    page = requests.post('http://finance.yahoo.com/quote/SPY')
    textfile = page.text
    num = textfile.find('CrumbStore')
    textfile2 = textfile[num:]
    num2 = textfile2.find('QuotePageStore') - 3
    textfile3 = textfile2[:num2]
    num3 = textfile3.rfind(':') + 1
    textfile4 = textfile3[num3:]
    textfile4.replace('"','')
    return str(textfile4)