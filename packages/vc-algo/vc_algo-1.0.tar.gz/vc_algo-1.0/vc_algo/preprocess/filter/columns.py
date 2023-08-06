import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

# ref: 基于sklearn的自定义转换器，用于整合到pipeline中实现标准化机器学习流水线 https://www.icode9.com/content-4-90790.html

class DropColumns(BaseEstimator, TransformerMixin):
    def __init__(self, drop_list):
        self.drop_list = drop_list

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        useful_columns = [x for x in list(X.columns) if (x not in self.drop_list)]
        df = X[useful_columns].copy()

        return df

class PickUpColumns(BaseEstimator, TransformerMixin):
    def __init__(self, pick_up_list):
        self.pick_up_list = pick_up_list

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        useful_columns = [x for x in list(X.columns) if (x in self.pick_up_list)]
        df = X[useful_columns].copy()

        return df
