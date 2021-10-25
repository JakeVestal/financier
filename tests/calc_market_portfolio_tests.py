import unittest
import pandas as pd
from financier import calc_market_portfolio

class mp_testcase(unittest.TestCase):
    df = pd.read_csv('../tests/data/10stocks.csv')
    def test_noshorts(self):
        calc_market_portfolio(df,allow_short="No")
    def test_shorts(self):
        calc_market_portfolio(df,allow_short="Yes")
