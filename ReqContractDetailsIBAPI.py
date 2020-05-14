  
# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is an API app for Interactive Brokers API, it requests and prints line by line data to screen.
#It can be found in its entirety on YouTube in the IB Python API videos by IB
#Need more functionality - use pandas DataFrame object

#API Access
#Double check your CWD
import os
os.chdir('Z:/DirectoryLocation/pythonclient/')
print(os.getcwd())

#Import modules
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import Contract
from threading import Thread
import queue
import datetime
import time

#Create app class w/ inheritance
class TestApp(EWrapper, EClient):
    #Overwriting
    def __init__(self):
        EClient.__init__(self, self)
    #Overwriting
    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)
    #Overwriting    
    def contractDetails(self, reqId, contractDetails):
        print("contractDetails: ", reqId, " ", contractDetails)
#Create main function
def main():
    #Call test app
    app = TestApp()
    #Call to connect
    app.connect("127.0.0.1", 7497, 0)
    #Create contract object    
    contract = Contract()
    #Define contract object
    contract.symbol = "AAPL"
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"
    contract.primaryExchange = "NASDAQ"
    #Request contract details
    app.reqContractDetails(1, contract)   
    #Initialize
    app.run()
    
#Run    
if __name__ == "__main__":
    main()
