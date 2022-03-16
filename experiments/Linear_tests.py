import sys

sys.path.append('..')
import pandas as pd
from sklearn.linear_model import LinearRegression
from utilities.Algorithm_params_generator import *
from utilities.Normalization import *
from utilities.Split import *


if __name__ == '__main__':
    # df = pd.read_csv("../data/created/Main_data.csv", header=0)
    df = pd.read_csv("../data/created/tmp_data.csv", header=0)
    X_train, X_test, y_train, y_test = split_one_train_one_test(df)
    #X_train, X_test, y_train, y_test = normalize(X_train, X_test, y_train, y_test)

    reg = LinearRegression()

    params_dict = dict(normalize=[True, False])
    best_grid, best_score = iterate_over_params(reg, params_dict, X_train, X_test, y_train, y_test)