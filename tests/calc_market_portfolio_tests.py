import os
import unittest
import pandas as pd
from financier import Portfolio

class MarketPortfolioTestCase(unittest.TestCase):
    print("----")
    print(os.getcwd())

    def setUp(self):
        df = pd.read_csv('../tests/data/10stocks.csv')
        exp_ret = []
        exp_vol = []
        for (stock,returns) in df.iteritems():
            exp_ret.append(np.mean(returns.values))
            exp_vol.append(np.std(returns.values))
        exp_cov = df.cov(min_periods=None, ddof=0).values
        tickers = df.columns
        self.portfolio = Portfolio(tickers, exp_ret, exp_vol, exp_cov)
    def test_noshorts(self):
        result = self.portfolio.optimize(rf=.25, allow_short=None).fun
        self.assertEqual(round(result,2), round(-0.4968591918232762,2))
    def test_shorts(self):
        result = self.portfolio.optimize(rf=.25, allow_short=None).fun
        self.assertEqual(round(result,2), round(-0.5472016099820182,2))

if __name__ == '__main__':
    unittest.main()