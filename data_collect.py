import pandas as pd
import pandas_datareader as w 
import numpy as np 
import statsmodels.api as s 
import matplotlib.pyplot as plt 
from statsmodels.tsa.stattools import adfuller



p_pairs = ['ETH-USD', 'SOL-USD']   # permissable pairs, you may alter this for top x pairs in volume
                                    # or whatever other metric


class Pair():


    def __init__(self, pairx, pairy):
        if pairx and pairy in p_pairs:
            self.pairx = pairx
            self.pairy = pairy
        else:
            self.pairx = None
            self.pairy = None
    
    def returns(self, lookback):
        if self.pairx and self.pairy:
            x = w.get_data_yahoo(self.pairx, start=lookback[0], end=lookback[1])
            y = w.get_data_yahoo(self.pairy, start=lookback[0], end=lookback[1])
            self.x_returns = x['Adj Close']
            self.y_returns = y['Adj Close']
            return self.x_returns, self.y_returns
        else:
            print('Pairs not permissable')
    
    def ols(self):
        if self.pairx and self.pairy:
            x = s.add_constant(self.x_returns)        
            model = s.OLS(self.y_returns, x)
            self.res = model.fit()
            return f'residuals are \n {self.res.resid}'
        else:
            print('Pairs not permissable')

    def adf(self):
        a = adfuller(self.res.resid)
        plt.plot(self.res.resid)
        plt.title(f'{self.pairx} / {self.pairy} spread \n adf-p value = {a[1]:3f}')
        plt.show()
        return f'engle-granger params for {self.pairx} and {self.pairy} \n {a}'

lookback1 = ['2022-01-01', '2022-10-12']

btc_sol = Pair('ETH-USD', 'SOL-USD')

print(btc_sol.returns(lookback1))
print(btc_sol.ols())
print(btc_sol.adf())


