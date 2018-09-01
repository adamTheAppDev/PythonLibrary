# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 16:20:46 2017

@author: AmatVictoriaCuramIII
"""

import numpy as np
from pandas_datareader import data
import pandas as pd
from RSIaggregate import RSIaggregate
q = data.DataReader('^GSPC', 'yahoo', start='01/01/1950', end='01/01/1972')
