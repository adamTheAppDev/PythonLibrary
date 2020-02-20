# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is an older version of a directory scanning and sorting tool

#Define function
def DatabaseAgeScanner(MinAge):
    #Get modules
    from SAge import SAge
#    from SAverageReturn import SAverageReturn
#    from SCoeffVar import SCoeffVar
#    from STrend import STrend
#    from SRelStrInd import SRelStrInd
#    from DayOverAverageRollingVolume import DayOverAverageRollingVolume
#    from SAverageRollingVolume import SAverageRollingVolume
#    from SAdjustedClose import SAdjustedClose
#    from pandas import read_csv
    from DatabaseGrabber import DatabaseGrabber
#    from SCommodityChannelIndex import SCommodityChannelIndex
    import os
    
    #Variable assignment
    counter = 1
    refinedportfolio = []
    #import the CSV
    #df = read_csv('goodsymbols.csv', sep = ',')
    #df = df[300]
    #symbols = df.Symbol.values
    #Assign tickers for scanning
    port = os.listdir('F:\\Users\\Username\\DirectoryLocation')
    #print(symbols)
    #For all stocks in list
    for s in port:
        try:
            #Iteration tracking
            print(counter)
            counter = counter + 1
            #Request data
            q = DatabaseGrabber(s)    
            #If passes age constraint
            if SAge(q) > MinAge:
    #            if float(SAdjustedClose(q)) > 5:
    #                if float(SAverageRollingVolume(q)) > 500000:
    #                    if float(STrend(q)) > 0.05:
    #                        if float(SRelStrInd(q)) < 30:
    #                            if float(SCommodityChannelIndex(q)) < -80:
                        #   ask another if or do commands
                #List ticker and add to list that passes scan
                print(s)
                refinedportfolio.append(s)
    #                            else:
    #                                continue
    #                        else:
    #                            continue
    #                    else:
    #                        continue
    #                else:
    #                    continue
    #            else:
    #                continue
            else:
                continue
    
    
    #                ) > 500000 and sum( and sum(SRelStrInd(q)) < 30:
            
    #              and sum(DayOverAverageRollingVolume(q)
    #        ) > 5 and sum(SAverageReturn(q)) < .02 and sum(SCoeffVar(q)
    #        ) < 1:
        except OSError:
            pass
    #List refined portfolio
    return refinedportfolio
