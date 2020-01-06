# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 11:04:18 2017

@author: AmatVictoriaCuramIII
"""

#Here is a code graveyard for unused code that might need to be used later...


#CSV requests yahoo

#firsthalf = "https://query1.finance.yahoo.com/v7/finance/download/" #insert ticker and add secondhalf
#secondhalf = "?period1=-630950400&period2=1592694000&interval=1d&events=history&crumb=1.ZWRp1I9ZS" #1950 - most recent
#nocrumb = "?period1=-630950400&period2=1592694000&interval=1d&events=history&crumb="
#df['URL'] = firsthalf + df['Symbol'] + secondhalf
#df['MainURL'] = 'https://finance.yahoo.com/quote/' + df['Symbol'] + '/history?p='+ df['Symbol']
#df = df[4623:]
#irequest = requests.get(df['MainURL'][0])
#cookie = irequest.cookies['B']
#r = requests.get(mainurl)
#BigCookie = r.headers['set-cookie']
#BigCookieList = BigCookie.split(sep=';')
#Cookie = r.cookies['B']
#print(Cookie)
#CookieDict = {'B' : Cookie}
#web.open(url2, new = 2)
#mainurl = "https://finance.yahoo.com/quote/" + ticker + "/history?p=" + ticker