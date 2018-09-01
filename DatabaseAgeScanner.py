# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 23:29:44 2017

@author: AmatVictoriaCuramIII
"""
#Get modules
def DatabaseAgeScanner(MinAge):
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
    
    #Got to get that payback!!
    counter = 1
    #import the CSV
    #df = read_csv('goodsymbols.csv', sep = ',')
    #df = df[300]
    #symbols = df.Symbol.values
    port = os.listdir('F:\\Users\\AmatVictoriaCuram\\Database')
    refinedportfolio = []
    #print(symbols)
    for s in port:
        try:
            print(counter)
            counter = counter + 1
            q = DatabaseGrabber(s)        
            if SAge(q) > MinAge:
    #            if float(SAdjustedClose(q)) > 5:
    #                if float(SAverageRollingVolume(q)) > 500000:
    #                    if float(STrend(q)) > 0.05:
    #                        if float(SRelStrInd(q)) < 30:
    #                            if float(SCommodityChannelIndex(q)) < -80:
                        #   ask another if or do commands
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