import numpy as np
import pandas as pd
def exp_cov(df):
    cov_matrix = df.cov(min_periods=None, ddof=0).values
    return cov_matrix