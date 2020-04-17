# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is part of a multithreading tool to speed up brute force optimization - looks under construction

#Import modules
from multithreadADXStratOpt import multithreadADXStratOpt
import numba as nb
import time as t
#Start timer
start = t.time()
#Assign function
f_nb = (multithreadADXStratOpt)
#End timer
end = t.time()
#Timer stats
print(end-start,'seconds later..')
#Print result
print(f_nb)
