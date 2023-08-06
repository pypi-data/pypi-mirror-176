import os.path

import joblib
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

# 1 传入数据集
X, y = make_classification(random_state=0)

# 2 分割数据集
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

# 3 准备pipeline
pipe = Pipeline([('scaler', StandardScaler()), ('svc', SVC())])

# 4 训练pipeline
pipe.fit(X_train, y_train)

# 5 预测pipeline
pipe.predict(X_test)

# 5 直接打分
pipe.score(X_test, y_test)

# 6 保存pipeline到当前目录
cwd = '/home/lyf/quant/vc_algo/vc_algo/example/pipeline' # 自行修改
model_path = os.path.join(cwd, 'basic_sklearn_pipe.pickle')
joblib.dump(pipe, model_path, compress=9)

# 7 读取pipeline，并transform
new_pipe = joblib.load(model_path)
print(new_pipe)
new_pipe.predict(X_train)
