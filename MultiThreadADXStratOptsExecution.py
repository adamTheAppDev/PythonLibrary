# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 14:52:56 2017

@author: AmatVictoriaCuramIII
"""
from multithreadADXStratOpt import multithreadADXStratOpt
import numba as nb
import time as t
start = t.time()
f_nb = (multithreadADXStratOpt)
end = t.time()
print(end-start,'seconds later..')
print(f_nb)
