# 仅供参考
# ref: 基于sklearn的自定义转换器，用于整合到pipeline中实现标准化机器学习流水线 https://www.icode9.com/content-4-90790.html

import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class IVTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, target_column=' ', label_column=' ', positive_label=[0], iv=0, woe=0):
        self.target_column = target_column
        self.label_column = label_column
        self.positive_label = positive_label
        self.iv = iv
        self.woe = woe

    def fit(self, df_name, y=None):
        if len(df_name[self.label_column].unique()) == 2:
            pos_label, neg_label = df_name.loc[:, self.label_column].unique()
            pos_counts = df_name[df_name[self.label_column] == pos_label][self.target_column].value_counts()
            neg_counts = df_name[df_name[self.label_column] == neg_label][self.target_column].value_counts()

            pos_total = df_name[self.label_column].value_counts()[pos_label]
            neg_total = df_name[self.label_column].value_counts()[neg_label]

            pos_rate = pos_counts / pos_total
            neg_rate = neg_counts / neg_total

            self.woe = np.log(pos_rate / neg_rate)
            self.iv = np.sum((pos_rate - neg_rate) * self.woe)

            return self

        elif len(df_name[self.label_column].unique()) > 2:
            new_label = np.array(['pos' if x in self.positive_label else 'neg' for x in df_name[self.label_column]])

            pos_total = (new_label == 'pos').sum()
            neg_total = (new_label == 'neg').sum()

            pos_counts = df_name.loc[new_label == 'pos', self.target_column].value_counts()
            neg_counts = df_name.loc[new_label == 'neg', self.target_column].value_counts()

            pos_rate = pos_counts / pos_total
            neg_rate = neg_counts / neg_total

            self.woe = np.log(pos_rate / neg_rate)
            self.iv = np.sum((pos_rate - neg_rate) * self.woe)

            return self

        elif len(df_name[self.label_column].unique()) < 2:

            print("Label needs at least 2 classes. The calculation cannot be executed.")

            return self

    def transform(self, df_name):
        df_name.loc[:, self.target_column] = df_name.loc[:, self.target_column].map(self.woe)

        return df_name