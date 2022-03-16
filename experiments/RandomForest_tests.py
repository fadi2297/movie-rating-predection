import sys

sys.path.append('..')
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from utilities.Algorithm_params_generator import *
from utilities.Normalization import *
from utilities.Split import *

if __name__ == '__main__':
    # df = pd.read_csv("../data/created/Main_data.csv", header=0)
    df = pd.read_csv("../data/created/tmp_data.csv", header=0)
    X_train, X_test, y_train, y_test = split_one_train_one_test(df)
    X_train, X_test, y_train, y_test = normalize(X_train, X_test, y_train, y_test)

    reg = RandomForestRegressor()

    params_dict = dict(n_estimators=[ 20, 100,500,1000], max_depth=[5, 10, 50,None])
    best_grid, best_score = iterate_over_params(reg, params_dict, X_train, X_test, y_train, y_test)

#--------------------------------------------
    params_dict = dict(n_estimators=[1000 ,2000,3000], max_depth=[None])
    best_grid, best_score = iterate_over_params(reg, params_dict, X_train, X_test, y_train, y_test)
