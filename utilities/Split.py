import sys

sys.path.append("..")

from sklearn.model_selection import train_test_split


def spilt_random(df):
    x = df.drop('average rating', axis=1)
    y = df['average rating']
    return train_test_split(x, y, test_size=0.2, random_state=42)


def split_one_train_one_test(df):
    df = df.sort_values(by=['year', 'month'])
    test = df[df.index % 7 == 0]
    train = df[df.index % 7 != 0]

    X_train = train.drop(['average rating'], axis=1)
    y_train = train['average rating']

    X_test = test.drop(['average rating'], axis=1)
    y_test = test['average rating']
    return X_train, X_test, y_train, y_test


def split_9_train_9_test(df):
    df = df.sort_values(by=['year', 'month'])
    test = df[df.index % 5 == 0]
    train = df[df.index % 5 != 0]

    train_lists, test_lists = [], []
    amount_each_set = (len(df) - 1) / 9
    i = (len(df) - 1) / 9
    while i < len(df):
        cond_test = (test.index >= i - amount_each_set) & (test.index < i)
        test_i = test[cond_test]
        cond_train = (train.index >= i - amount_each_set) & (train.index < i)
        train_i = train[cond_train]
        train_lists.append(train_i)
        test_lists.append(test_i)
        i += amount_each_set

    return train_lists, test_lists
