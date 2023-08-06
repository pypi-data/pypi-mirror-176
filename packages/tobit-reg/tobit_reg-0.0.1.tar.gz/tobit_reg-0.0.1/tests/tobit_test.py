import unittest
import pandas as pd
import os

from src.tobit_reg.tobit_reg import TobitRegression


class TobitTest(unittest.TestCase):
    def setUp(self) -> None:
        self.df = pd.read_csv(os.path.join("data", "tobit_unittest.csv"))
        self.tobit = TobitRegression(low=200, high=800)

    def test_regression(self):
        x = self.df[["read", "math", "prog"]].values
        y = self.df.loc[:, "apt"].values
        res = self.tobit.fit(x, y, include_constant=True, categorical=(2,))
        df = pd.DataFrame.from_records([res.parameters], columns=res.varnames)
        print(df)
        print(res.history)
        self.assertIsNotNone(res)

