# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 17:00:32 2019

@author: AmatVictoriaCuramIII
"""

#Cut Pak quote generator for Jujin PDFs

#Import
import os
import time as t
import numpy
import pandas as pd
import math
import PyPDF2
import tabula

#Start timer
start = t.time()
#Assign Jujin PDF quote folder
if not os.path.exists('F:\\Users\\AmatVictoriaCuram\\JUJIN_PDFS'):
    os.makedirs('F:\\Users\\AmatVictoriaCuram\\JUJIN_PDFS')
#Assign Jujin CSV folder
if not os.path.exists('F:\\Users\\AmatVictoriaCuram\\JUJIN_CSVS'):
    os.makedirs('F:\\Users\\AmatVictoriaCuram\\JUJIN_CSVS')
#Assign Cut Pak post-processing destination folder
if not os.path.exists('F:\\Users\\AmatVictoriaCuram\\CUTPAK_QUOTES'):
    os.makedirs('F:\\Users\\AmatVictoriaCuram\\CUTPAK_QUOTES')
#Assign Cut Pak template folder
if not os.path.exists('F:\\Users\\AmatVictoriaCuram\\CUTPAK_TEMPLATES'):
    os.makedirs('F:\\Users\\AmatVictoriaCuram\\CUTPAK_TEMPLATES')
#Assign Cut Pak inventory folder
if not os.path.exists('F:\\Users\\AmatVictoriaCuram\\CUTPAK_INVENTORY'):
    os.makedirs('F:\\Users\\AmatVictoriaCuram\\CUTPAK_INVENTORY')    
    
#For each quote in JujinPDFs folder
JujinPDFlist = list(os.listdir('F:\\Users\\AmatVictoriaCuram\\JUJIN_PDFS'))
#Open Quote
for j in JujinPDFlist:
    JujinQuoteLocation = 'F:\\Users\\AmatVictoriaCuram\\JUJIN_PDFS\\' + j
    #Read Quote 
    JujinPDFFileObject = open(JujinQuoteLocation, 'rb')
    TabulaObject = tabula.read_pdf(JujinQuoteLocation)
    #Reformat Quote
    JujinPDFReaderObject = PyPDF2.PdfFileReader(JujinPDFFileObject)
    #Access PageObject
    PageObject = JujinPDFReaderObject.getPage(0)
    TextObject = PageObject.extractText()
#    print(TextObject)
#Add idiosyncratic client info to data structure

#Apply result to Cut Pak quote

#Save Cut Pak quote to destination

#End timer
end = t.time()
duration = end - start
#Text
print('Total process took ' + str(duration) + ' seconds.')