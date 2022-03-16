import sys

sys.path.append("..")
from sklearn.model_selection import ParameterGrid


def iterate_over_params(reg, param_dict, X_train, X_test, y_train, y_test):
    best_score = -1
    best_comb = {}
    for comb in ParameterGrid(param_dict):
        reg.set_params(**comb)
        reg.fit(X_train, y_train)
        score = reg.score(X_test, y_test)
        print(comb, 'Score: ', score)

        if score > best_score:
            best_score, best_comb = score, comb

    print('Best Score:', best_score)
    print('Best Parameters:', best_comb)
    return best_comb, best_score
