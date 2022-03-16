import sys

sys.path.append('..')
import pandas as pd
from sklearn.ensemble import AdaBoostRegressor
from sklearn.tree import DecisionTreeRegressor
from utilities.Algorithm_params_generator import *
from utilities.Normalization import *
from utilities.Split import *



if __name__ == '__main__':
    # df = pd.read_csv("../data/created/Main_data.csv", header=0)
    df = pd.read_csv("../data/created/tmp_data.csv", header=0)

    X_train, X_test, y_train, y_test = split_one_train_one_test(df)
    X_train, X_test, y_train, y_test = normalize(X_train, X_test, y_train, y_test)

    reg = AdaBoostRegressor()
    dt = DecisionTreeRegressor(max_depth=7,min_samples_leaf=15,splitter='best')
    params_dict = dict(base_estimator=[dt], n_estimators=[1, 15, 50, 100], loss=['linear', 'exponential'])
    best_grid, best_score = iterate_over_params(reg, params_dict, X_train, X_test, y_train, y_test)
