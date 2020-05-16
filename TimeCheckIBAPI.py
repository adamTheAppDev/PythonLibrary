# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a basic API app for Interactive Brokers API from IB API on youtube

#API Access
#Import module
import os
#Check your CWD
os.chdir('Z:/sauce/pyclient/')
#Display CWD
print(os.getcwd())

#Import modules
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import Contract
from threading import Thread
import queue
import datetime
import pandas as pd 

#Define class
class TestApp(EWrapper, EClient):
    #Initialize
    def __init__(self):
        EClient.__init__(self, self)
    #Overwrite
    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)
    #Overwrite
    def contractDetails(self, reqId, contractDetails):
        print("contractDetails: ", reqId, " ", contractDetails)

#Define function
def main():
    #Call test app
    app = TestApp()
    #Call to connect
    app.connect("127.0.0.1", 7497, 0) 
    #Functionality
    print("serverVersion:%s connectionTime:%s" % (app.serverVersion(),
                                                      app.twsConnectionTime()))
                                                  
    app.run()
    
#Run    
if __name__ == "__main__":
    main()
