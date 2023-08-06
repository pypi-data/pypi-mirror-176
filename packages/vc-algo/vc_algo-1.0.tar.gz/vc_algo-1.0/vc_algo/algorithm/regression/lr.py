# ref : Developing custom scikit-learn transformers and estimators https://ploomber.io/blog/sklearn-custom/
# ref : Developing scikit-learn estimators https://scikit-learn.org/stable/developers/develop.html
import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.linear_model import LinearRegression
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted


class FactorLinearRegression(BaseEstimator, RegressorMixin):

    def __init__(self, est_class=LinearRegression, **kwargs):
        self.est_class = est_class
        # kwargs depend on the model used, so assign them whatever they are
        for key, value in kwargs.items():
            setattr(self, key, value)
        # 必须设置参数名称
        self._param_names =list(kwargs.keys())

    def fit(self, X, y, **kwargs):
        est_kwargs = self.get_params()
        # remember the trailing underscore
        self.model_ = self.est_class(**est_kwargs)
        self.model_.fit(X, y, **kwargs)
        # fit must return self
        return self

    def predict(self, X):

        # Check if fit has been called
        check_is_fitted(self)

        # Input validation
        X = check_array(X)

        y_pred = self.model_.predict(X)

        return y_pred

    # 模型打分
    def score(self, X, y, **kwargs):
        return self.model_.score(X, y, **kwargs)

    # 获取参数
    def get_params(self, deep=True):
        # Note: we are ignoring the deep parameter
        # this will not work with estimators that have sub-estimators
        # see https://scikit-learn.org/stable/developers/develop.html#get-params-and-set-params
        return {param: getattr(self, param)
                for param in self._param_names}

    # 设置参数
    def set_params(self, **parameters):
        for parameter, value in parameters.items():
            setattr(self, parameter, value)
        return self

    # 查看训练后的模型的参数
    def __getattr__(self, key):
        if key != 'model_':
            if hasattr(self, 'model_'):
                return getattr(self.model_, key)
            else:
                return getattr(self.est_class, key)
        else:
            raise AttributeError(
                "'{}' object has no attribute 'model_'".format(type(self).__name__))