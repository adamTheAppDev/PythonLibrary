# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#Random (uniformly distributed) weighting tool...

#Random Weights = 1
#Define function
def RandomWeight(num_assets):
    #Import modules
    import numpy as np
    #Assign random values
    Weight_Array = np.random.rand(num_assets)
    #Output
    return Weight_Array / sum(Weight_Array)
