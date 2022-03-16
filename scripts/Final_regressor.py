import sys

sys.path.append('..')
from joblib import dump
from experiments.K_features_tests import *



if __name__ == '__main__':
    df = pd.read_csv('../data/created/Main_data.csv', header=0)
    print('Creating The Final Model!')
    # CREATING FINAL REGRESSOR
    # lst_features = getTopFeatures(df, k, f_regression)
    # X_train, X_test, y_train, y_test = split_one_train_one_test(df)
    df = df.sort_values(by=['year', 'month'])
    X_train = df.drop(['average rating'], axis=1)
    y_train = df['average rating']
    X_train, X_test, y_train, y_test = normalize(X_train,X_train,y_train,y)

    GB_best_reg = GradientBoostingRegressor(max_depth=5, n_estimators=300 )
    GB_best_reg.fit(X_train, y_train)
    dump(GB_best_reg, 'our_model.joblib')

#-------------------------------------------------------------------
    # RF_best_reg = RandomForestRegressor(max_depth=None, n_estimators=50)
    # RF_best_reg.fit(X_train, y_train)
    # dump(RF_best_reg, 'our_model.joblib')

#-----------------------------------------------------------------------
    # Linear_best_reg = LinearRegression(normalize=True)
    # Linear_best_reg.fit(X_train, y_train)
    # dump(Linear_best_reg, 'our_model.joblib')

