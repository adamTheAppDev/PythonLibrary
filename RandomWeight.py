# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 15:35:50 2017

@author: AmatVictoriaCuramIII
"""

#Random Weights = 1
def RandomWeight(num_assets):
    import numpy as np
    Weight_Array = np.random.rand(num_assets)
    return Weight_Array / sum(Weight_Array)