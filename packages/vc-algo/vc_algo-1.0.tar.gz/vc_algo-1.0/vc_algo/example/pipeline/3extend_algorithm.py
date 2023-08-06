import os.path

import joblib
import pandas as pd
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

# 1 传入数据集
n_features = 20
X, y = make_regression(random_state=0, n_features=n_features)
# 构建columns为后续的pick_up预处理做准备
X_columns = ['alpha' + str(i) for i in range(n_features)]
import numpy as np
pick_up_list = ['alpha' + str(i) for i in np.random.choice(n_features, 5, replace=False)]

# 2 分割数据集
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
X_train, X_test = pd.DataFrame(X_train), pd.DataFrame(X_test)
X_train.columns = X_test.columns = X_columns

# 3 准备pipeline
from vc_algo.preprocess.filter.columns import PickUpColumns
from vc_algo.algorithm.regression.lr import FactorLinearRegression
pipe = Pipeline([
    ('pick_up', PickUpColumns(pick_up_list=pick_up_list))
    , ('scaler', StandardScaler())
    , ('lr', FactorLinearRegression())
])

# 4 训练pipeline
pipe.fit(X_train, y_train)
print(pipe)

# 5 预测pipeline
pipe.predict(X_test)

# 6 直接打分分析
pipe.score(X_test, y_test)

# 7 保存pipeline到当前目录
cwd = '/home/lyf/quant/vc_algo/vc_algo/example/pipeline' # 自行修改
model_path = os.path.join(cwd, 'extend_algorithm.pickle')
joblib.dump(pipe, model_path, compress=9)

# 8 读取pipeline，并transform
new_pipe = joblib.load(model_path)
print(new_pipe)
new_pipe.predict(X_test)
