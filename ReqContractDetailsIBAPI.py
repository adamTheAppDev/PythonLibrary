# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 18:35:21 2018

@author: AmatVictoriaCuramIII
"""

#This is an API app for Interactive Brokers API, it requests and prints line by line data to screen.
#Need more functionality - use pandas DataFrame object 

#API Access
#Double check your CWD
import os
os.chdir('C:/source/pythonclient/')
print(os.getcwd())

#Add dependencies
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import Contract
from threading import Thread
import queue
import datetime
import time

class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
    
    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)
        
    def contractDetails(self, reqId, contractDetails):
        print("contractDetails: ", reqId, " ", contractDetails)

def main():
    app = TestApp()
    
    app.connect("127.0.0.1", 7497, 0)
        
    contract = Contract()
    contract.symbol = "AAPL"
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"
    contract.primaryExchange = "NASDAQ"

    app.reqContractDetails(1, contract)   

    app.run()
    
if __name__ == "__main__":
    main()
