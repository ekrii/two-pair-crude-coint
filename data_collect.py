import pandas as pd
import pandas_datareader as w 
import numpy as np 
import statsmodels.api as s 
import requests 
import matplotlib.pyplot as plt 
import json 

#x = [3,4,5,9,1,10,2]
#y = [4,4,9,1,2,3,1]

#x = s.add_constant(x)
#model = s.OLS(y, x)
#results = model.fit() 


# alpha vantage 

def handle_msg(msg):
    return msg.json() 

class Pair():

    p_pairs = []   # permissable pairs 


    def __init__(self, pairx, pairy):
        if pairx and pairy in self.p_pairs:
            self.pairx = pairx
            self.pairy = pairy
        else:
            None
    
    def returns(self, lookback):
        x = w.data(f'url/{self.pairx}/{lookback}')
        y = w.data(f'url/{self.pairy}/{lookback}')
        self.x_returns = x['Adj Close'].pctchange()
        self.y_returns = y['Adj Close'].pctchange()
        return x, y
    
    def ols(self):
        x = s.add_constant(self.x_returns)        
        model = s.OLS(self.y_returns, x)
        res = model.fit()
        return res 


    
btc_sol = Pair('btc', 'sol')
print(btc_sol.returns())



        