"""
Spyder Editor
"""

from YahooGrabber import YahooGrabber
import numpy as np
import time as t


ticker = 'UVXY'
lag = 15
atrwindow = 20
closewindow = 15
ranger = range(0,closewindow)
s = YahooGrabber(ticker)
start = t.time()
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)
s['RateOfChange'] = (s['Adj Close'] - s['Adj Close'].shift(lag)
                                  ) / s['Adj Close'].shift(lag)

s['UpMove'] = s['High'] - s['High'].shift(1)
s['DownMove'] = s['Low'] - s['Low'].shift(1)
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)
s['Method1'] = s['High'] - s['Low']
s['Method2'] = abs((s['High'] - s['Close'].shift(1)))
s['Method3'] = abs((s['Low'] - s['Close'].shift(1)))
s['Method1'] = s['Method1'].fillna(0)
s['Method2'] = s['Method2'].fillna(0)
s['Method3'] = s['Method3'].fillna(0)
s['TrueRange'] = s[['Method1','Method2','Method3']].max(axis = 1)
s['AverageTrueRange'] = s['TrueRange'].rolling(window = atrwindow,
                                center=False).mean()

s['ZeroLine'] = 0

s['OGRegime'] = np.where(s['RateOfChange'] > .25, -1, 0)
s['Regime'] = s['OGRegime']
for r in ranger:
    s['Regime'] = np.where(s['Regime'].shift(1) == -1, -1, s['Regime'])

s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
s['Strategy'] = s['Strategy'].fillna(0)
s['Strategy1'] = s['Strategy'] + 1
s['Multiplier'] = s['Strategy'].cumsum().apply(np.exp)
drawdown =  1 - s['Multiplier'].div(s['Multiplier'].cummax())
s['drawdown'] =  1 - s['Multiplier'].div(s['Multiplier'].cummax())

#basic position sizing

s['Position'] = 0
s['Position'][s['drawdown'] > .4] = .1
s['Position'][s['drawdown'] < .4] = .06
s['Position'][s['drawdown'] < .2] = .03
MaxDD = max(drawdown)
s['NewRegime'] = s['Regime'] * s['Position']

dailyreturn = s['Strategy'].mean()

dailyvol = s['Strategy'].std()
sharpe =(dailyreturn/dailyvol)
#s[['LogRet','Strategy']].cumsum().apply(np.exp).plot(grid=True,
#                                 figsize=(8,5))
s['NewStrategy'] = (s['NewRegime']).shift(1)*s['LogRet']  
s['NewStrategy'].fillna(0)
s['NewMultiplier'] = s['NewStrategy'].cumsum().apply(np.exp)      

s[['NewStrategy']].cumsum().apply(np.exp).plot(grid=True,
                                figsize=(8,5))
              
Length = len(s['LogRet'])
Range = range(0,Length)
print(MaxDD*100, '% = Max Drawdown')

end = t.time()
print((end - start), ' seconds later.')