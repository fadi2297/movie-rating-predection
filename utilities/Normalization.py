import sys

sys.path.append("..")



def extract_min_max_x(df):
    df = df.to_numpy()
    min_list, max_list = [], []
    for i in range(len(df[0])):
        tmp_list = [row[i] for row in df]
        min_list.append(min(tmp_list))
        max_list.append(max(tmp_list))
    return min_list, max_list


def extract_min_max_y(arr):
    return min(arr), max(arr)


def normalize_x(df, min_list, max_list):
    for idx, f in enumerate(df.columns):
        df[f] = (df[f] - min_list[idx]) / (max_list[idx] - min_list[idx])
    return df


def normalize_y(arr, min_val, max_val):
    norm_arr = []
    for val in arr:
        new_val = (val - min_val) / (max_val - min_val)
        norm_arr.append(new_val)
    return norm_arr


def normalize(X_train, X_test, y_train, y_test):
    min_list, max_list = extract_min_max_x(X_train)
    min_val, max_val = extract_min_max_y(y_train)

    X_train = normalize_x(X_train, min_list, max_list)
    X_test = normalize_x(X_test, min_list, max_list)

    y_train = normalize_y(y_train, min_val, max_val)
    y_test = normalize_y(y_test, min_val, max_val)

    return X_train, X_test, y_train, y_test


def reverse_normalization(val, y_train):
    min_val, max_val = extract_min_max_y(y_train)
    return val * (max_val - min_val) + min_val
