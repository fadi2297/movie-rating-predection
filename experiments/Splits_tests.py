import pandas as pd
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor

from utilities.Normalization import *
from utilities.Split import *


# from sklearn import metrics
# import numpy as np


def extract_x_y(df):
    x = df.drop(['average rating'], axis=1)
    y = df['average rating']
    return x, y


def test_splits(df, split_method):
    X_train, X_test, y_train, y_test = split_method(df)
    X_train, X_test, y_train, y_test = normalize(X_train, X_test, y_train, y_test)

    reg = AdaBoostRegressor()
    reg.fit(X_train, y_train)
    print('AdaBoostRegressor performance: ', reg.score(X_test, y_test))

    reg = DecisionTreeRegressor()
    reg.fit(X_train, y_train)
    print('DecisionTreeRegressor performance: ', reg.score(X_test, y_test))

    reg = GradientBoostingRegressor()
    reg.fit(X_train, y_train)
    print('GradientBoostingRegressor performance: ', reg.score(X_test, y_test))

    reg = KNeighborsRegressor()
    reg.fit(X_train, y_train)
    print('KNeighborsRegressor performance: ', reg.score(X_test, y_test))

    reg = LinearRegression()
    reg.fit(X_train, y_train)
    print('LinearRegression performance: ', reg.score(X_test, y_test))

    reg = RandomForestRegressor()
    reg.fit(X_train, y_train)
    print('RandomForestRegressor performance: ', reg.score(X_test, y_test))

    # y_pred = reg.predict(X_test)
    # y_pred = [reverse_normalization(y, df) for y in y_pred]
    # df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
    # print(df)

    # print('Mean of all the values:', )
    # print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
    # print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
    # print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))


def run_loop(reg, train_list, test_list, reg_name):
    score = 0
    for i in range(9):
        X_train, y_train = extract_x_y(train_list[i])
        X_test, y_test = extract_x_y(test_list[i])

        X_train, X_test, y_train, y_test = normalize(X_train, X_test, y_train, y_test)

        reg.fit(X_train, y_train)
        score += reg.score(X_test, y_test)

    print(reg_name, score / 9)


def test_sets_splits(df):
    train_list, test_list = split_9_train_9_test(df)
    reg = AdaBoostRegressor()
    run_loop(reg, train_list, test_list, 'AdaBoostRegressor performance: ')

    reg = DecisionTreeRegressor()
    run_loop(reg, train_list, test_list, 'DecisionTreeRegressor performance: ')

    reg = GradientBoostingRegressor()
    run_loop(reg, train_list, test_list, 'GradientBoostingRegressor performance: ')

    reg = KNeighborsRegressor()
    run_loop(reg, train_list, test_list, 'KNeighborsRegressor performance: ')

    reg = LinearRegression()
    run_loop(reg, train_list, test_list, 'LinearRegression performance: ')

    reg = RandomForestRegressor()
    run_loop(reg, train_list, test_list, 'RandomForestRegressor performance: ')


if __name__ == '__main__':
    df = pd.read_csv("../data/created/Main_data.csv", header=0)

    print("Testing Random Split:")
    test_splits(df, spilt_random)

    print()
    print('------------------------------------------------------------')
    print()

    print('Testing One Train Set and One Test Set:')
    test_splits(df, split_one_train_one_test)

    print()
    print('------------------------------------------------------------')
    print()

    print('Testing 9 Train Set and 9 Test Set:')
    test_sets_splits(df)
