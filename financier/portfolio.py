import numpy as np
from scipy import optimize


class Portfolio:

    def __init__(self, tickers, exp_ret, exp_vol, exp_cov):
        self.tickers = tickers
        self.exp_ret = exp_ret
        self.exp_vol = exp_vol
        self.exp_cov = exp_cov

    def optimize(self, rf=0, tolerance=10e-6, allow_short=None):
        #add function for shorting later
        portfolio_size = len(self.exp_ret)

        #objective function (sharpe ratio = (port_ret - rf)/port_vol)
        def sharpe(weights, exp_ret, exp_vol):
            port_ret = np.dot(self.exp_ret, weights)
            weights_matrix = np.array(weights).reshape(-1,1)*np.array(weights)
            port_vol = np.sqrt(np.sum(np.multiply(weights_matrix, self.exp_cov)))
            sharpe = -((port_ret - rf)/port_vol)
            return sharpe
            #initial guess
        xinit = np.repeat(1/portfolio_size, portfolio_size)

        #bounds: (0,1) if allow_short=='No', None if allow_short=='Yes',
        if allow_short == None:
            lb=0
            ub=1
            bounds = tuple([(lb,ub) for x in xinit])
        else:
            bounds = None

        #constraint: sum(weights)=1
        cons = ({'type': 'eq', 'fun': lambda xinit: np.sum(xinit)-1})

        #minimization solver
        opt = optimize.minimize(sharpe,x0=xinit, args= (self.exp_ret, self.exp_vol),
                                method = 'SLSQP', bounds=bounds, constraints=cons,tol=10**-3)
        result = opt

        #print optimal sharpe and weights
        optimal_sharpe = -result.fun
        port_exp_ret = np.dot(self.exp_ret, result.x)
        weights_matrix = np.array(result.x).reshape(-1,1)*np.array(result.x)
        port_exp_vol = np.sqrt(np.sum(np.multiply(weights_matrix, self.exp_cov)))
        return opt



