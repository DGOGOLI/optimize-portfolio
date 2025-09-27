import pandas as pd
import numpy as np
from scipy.optimize import minimize


class Optimizer():

    def __init__(self, data: pd.DataFrame, trading_days: int):
        
        self.data = data
        self.trading_days = trading_days
        self.daily_returns = self.compute_daily_return()
        self.annual_returns = self.compute_annual_return()
        self.cov = self.compute_cov()


    def compute_daily_return(self)-> pd.DataFrame:

        daily_returns = np.log(self.data / self.data.shift(1)).dropna()

        return daily_returns
    
    def compute_annual_return(self)-> float:

        return self.daily_returns.mean() * self.trading_days
    
    def compute_cov(self):

        return self.daily_returns.cov() * self.trading_days
    
    def compute_volatility(self, weights):

        return np.sqrt(weights.T @ self.cov @ weights)
    
    def compute_min_volatility_weights(self):

        n_assets = len(self.annual_returns)
        init_guess = n_assets * [1./n_assets] 
        bounds = tuple((0, 1) for _ in range(n_assets))
        constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w)-1})

        min_volatility_portfolio = minimize(
        fun = self.compute_volatility,
        x0 = init_guess,
        args = (),
        method = 'SLSQP',
        bounds = bounds,
        constraints = constraints
        )

        opt_weights = min_volatility_portfolio.x

        return opt_weights
    
    def compute_portfolio_return(self, weights):

        return round(np.dot(weights, self.annual_returns), 2)