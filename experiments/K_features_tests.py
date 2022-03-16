import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression, mutual_info_regression
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor

from utilities.Normalization import *
from utilities.Split import *

features = ['year', 'month', 'genre', 'duration', 'first country', 'second country', 'Is second country',
            'first language', 'second language', 'Is second language', 'production company', 'budget',
            'first actor age', 'first actor amount of movies', 'first actor gender', 'second actor age',
            'second actor amount of movies', 'second actor gender', 'director amount of movies', 'average rating']

regression_name = ['DecisionTreeRegressor',
                   'AdaBoostRegressor',
                   'GradientBoostingRegressor',
                   'KNeighborsRegressor',
                   'LinearRegression',
                   'RandomForestRegressor']


def list_to_features(features_lst):
    return [features[i] for i in features_lst]


def Diff(li1, li2):
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return li_dif


def getTopFeatures(df, k, score_func):
    X_reg = df.iloc[:, 0:19]
    y_reg = df.iloc[:, 19]
    k_best = []
    tmp = []
    for i in range(k):
        selector = SelectKBest(score_func, k=i + 1)
        selector.fit(X_reg, y_reg)
        cols = selector.get_support(indices=True)
        cols = cols.tolist()
        k_best = k_best + Diff(cols, tmp)
        tmp = cols
    return k_best


def calc_results(df, reg, k_features_lst):
    results = []
    X_train, X_test, y_train, y_test = split_one_train_one_test(df)
    X_train, X_test, y_train, y_test = normalize(X_train, X_test, y_train, y_test)

    for k in k_features_lst:
        lst_features = getTopFeatures(df, k, f_regression)
        new_X_train = X_train[list_to_features(lst_features)]
        new_X_test = X_test[list_to_features(lst_features)]
        reg.fit(new_X_train, y_train)
        score = reg.score(new_X_test, y_test)
        results.append(score)
    #    print(k, score)

    return results


def plot_result_matrix(k_values, result_matrix, legend):
    for k in range(len(legend)):
        plt.plot(k_values, result_matrix[k], label=legend[k])
    plt.legend()
    plt.xticks(k_values)
    plt.title('regression score as a function of k')
    plt.xlabel('k')
    plt.ylabel('score')
    # plt.savefig('SelectKBestGraph.png')
    plt.show()


if __name__ == '__main__':
    df = pd.read_csv('../data/created/Main_data.csv', header=0)

    # checking different params for select k
    lst = getTopFeatures(df, 5, f_regression)
    lst = getTopFeatures(df, 5, mutual_info_regression)

    # choosing the best algorithm with best k
    algs_results = []
    k_values = [5, 7, 13, 15, 19]

    DT_best_reg = DecisionTreeRegressor(max_depth=7, min_samples_leaf=15, splitter='best')
    DT_results = calc_results(df, DT_best_reg, k_values)
    algs_results.append(DT_results)

    AB_best_reg = AdaBoostRegressor(base_estimator=DT_best_reg, loss='exponential', n_estimators=15)
    AB_results = calc_results(df, AB_best_reg, k_values)
    algs_results.append(AB_results)

    GB_best_reg = GradientBoostingRegressor(max_depth=5, n_estimators=300)
    GB_results = calc_results(df, GB_best_reg, k_values)
    algs_results.append(GB_results)

    KN_best_reg = KNeighborsRegressor(metric='manhattan', n_neighbors=20, weights='distance')
    KN_results = calc_results(df, KN_best_reg, k_values)
    algs_results.append(KN_results)

    Linear_best_reg = LinearRegression(normalize=True)
    Linear_results = calc_results(df, Linear_best_reg, k_values)
    algs_results.append(Linear_results)

    RF_best_reg = RandomForestRegressor(max_depth=None, n_estimators=1000)
    RF_results = calc_results(df, RF_best_reg, k_values)
    algs_results.append(RF_results)

    plot_result_matrix(k_values, algs_results, regression_name)
