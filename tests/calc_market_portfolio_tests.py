#import data + calculate stock exp returns,exp_vol
import unittest
import os.path
import pandas as pd
from financier import calc_market_portfolio

class calc_market_portfolio_test_case(unittest.TestCase):

    def setUp(self):
        self.market_portfolio =


df = pd.read_csv(os.path.join('data', '10stocks.csv'))
# import data + calculate stock exp returns,exp_vol
exp_ret = []
exp_vol = []
for (stock, returns) in df.iteritems():
    exp_ret.append(np.mean(returns.values))
    exp_vol.append(np.std(returns.values))
portfolio_size = len(df.columns)


