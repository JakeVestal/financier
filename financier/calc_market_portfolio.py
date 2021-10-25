
import numpy as np
from scipy import optimize

def calc_market_portfolio(df, rf=.25,allow_short='No'):
    #import data + calculate stock exp returns,exp_vol
    exp_ret = []
    exp_vol = []
    for (stock,returns) in df.iteritems():
        exp_ret.append(np.mean(returns.values))
        exp_vol.append(np.std(returns.values))
    portfolio_size = len(df.columns)

    #objective function (sharpe ratio = (port_ret - rf)/port_vol)
    def sharpe(weights, exp_ret, exp_vol):
        port_ret = np.dot(exp_ret, weights)
        weights_matrix = np.array(weights).reshape(-1,1)*np.array(weights)
        cov_matrix = df.cov(min_periods=None, ddof=0).values
        port_vol = np.sqrt(np.sum(np.multiply(weights_matrix, cov_matrix)))
        sharpe = -((port_ret - rf)/port_vol)
        return sharpe


    #initial guess
    xinit = np.repeat(1/portfolio_size, portfolio_size)

    #bounds: (0,1) if allow_short=='No', None if allow_short=='Yes',
    if allow_short == "No":
        lb=0
        ub=1
        bounds = tuple([(lb,ub) for x in xinit])
    else:
        bounds = None

    #constraint: sum(weights)=1
    cons = ({'type': 'eq', 'fun': lambda xinit: np.sum(xinit)-1})

    #minimization solver
    opt = optimize.minimize(sharpe,x0=xinit, args= (exp_ret, exp_vol),
                            method = 'SLSQP', bounds=bounds, constraints=cons,tol=10**-3)
    result = opt

    #print optimal sharpe and weights
    optimal_sharpe = -result.fun
    port_exp_ret = np.dot(exp_ret, result.x)
    weights_matrix = np.array(result.x).reshape(-1,1)*np.array(result.x)
    cov_matrix = df.cov(min_periods=None, ddof=0).values
    port_exp_vol = np.sqrt(np.sum(np.multiply(weights_matrix, cov_matrix)))
    print('Portfolio Expected Return: {0}'.format(port_exp_ret))
    print('Portfolio Expected Volatility: {0}'.format(port_exp_vol))
    print('Optimal Sharpe: {0}'.format(optimal_sharpe))
    print('Optimal Weights:')
    for i in range(len(df.columns)):
        print('{0}: {1}'.format(df.columns[i],result.x[i]))
    print(' ')
    return opt



