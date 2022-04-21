import pandas as pd
from joblib import load

# GENRE_CHOICES =(("0", "adult"), ("1", "action"), ("2", "adventure"), ("3", "animation"),
#                 ("4", "biography"), ("5", "comedy"), ("6", "crime"), ("7", "documentary"),
#                 ("8", "drama"), ("9", "family"), ("10", "fantasy"), ("11", "film-noir"),
#                 ("12", "history"), ("13", "horror"), ("14", "music"), ("15", "musical"),
#                 ("16", "mystery"), ("17", "romance"), ("18", "sci-fi"), ("19", "sport"),
#                 ("20", "thriller"), ("21", "war"), ("22", "western"))

genres_list = ['adult', 'action', 'adventure', 'animation', 'biography','comedy',
                'crime', 'documentary', 'drama', 'family', 'fantasy', 'film-noir',
                'history', 'horror', 'music', 'musical', 'mystery', 'romance',
                'sci-fi', 'sport','thriller', 'war', 'western']

def extract_countires():
    df = pd.read_csv("./static/my_app/csv/Countries.csv", header=0)
    return list(df['country'])

def extract_languages():
    df = pd.read_csv("./static/my_app/csv/Languages.csv", header=0)
    return list(df['languages'])

def extract_productions():
    df = pd.read_csv("./static/my_app/csv/Productions.csv", header=0)
    return list(df['production company'])

def extract_actors():
    df = pd.read_csv("./static/my_app/csv/actors_info.csv", header=0)
    return list(df['name'])

def extract_directors():
    df = pd.read_csv("./static/my_app/csv/directors_info.csv", header=0)
    return list(df['name'])

def correct_production_company(word):
    word = word.replace('-', ' ')
    word = word.replace('á', 'a')
    word = word.replace('ñ', 'n')
    word = word.replace('é', 'e')
    word = word.replace('í', 'i')
    word = word.replace('ó', 'o')
    word = word.replace('ö', 'o')
    word = word.replace('ü', 'u')
    return word

def create_pd(vec):
    selected = ['year', 'month', 'genre', 'duration', 'first country', 'second country', 'Is second country',
                'first language', 'second language', 'Is second language', 'production company', 'budget',
                'first actor age', 'first actor amount of movies', 'first actor gender', 'second actor age',
                'second actor amount of movies', 'second actor gender', 'director amount of movies']
    res = {}
    for key in selected:
        for value in vec:
            x = [value]
            res[key] = x
            vec.remove(value)
            break
    return pd.DataFrame(data=res)


def create_vec(data):
    vec = []
    year = int(data['date'].year)
    vec.append(year)
    vec.append(int(data['date'].month))

    genre_lst = []
    for index in data['genre']:
        genre_lst.append(genres_list[int(index)])
    genre_lst = sorted(genre_lst, key=str.lower)
    genres = (' '.join(genre_lst))
    df = pd.read_csv("./static/my_app/csv/Genres.csv", header=0).values
    genres_int = -1
    for row in df:
        if row[0] == genres:
            genres_int = row[1]
            break
    vec.append(genres_int)

    vec.append(data['duration'])
    vec.append(int(data['country1']))

    if int(data['country2']) == 0:
        vec.append(-1)
        vec.append(0)
    else:
        vec.append(int(data['country2']))
        vec.append(1)

    vec.append(int(data['language1'])-1)
    if int(data['language2']) == 0:
        vec.append(-1)
        vec.append(0)
    else:
        vec.append(int(data['language2'])-1)
        vec.append(1)

    df = pd.read_csv("./static/my_app/csv/Productions.csv", header=0).values
    production = data['production']
    for row in df:
        if production.lower() in correct_production_company(row[0]).lower():
            production = row[1]
            break
    vec.append(production)

    vec.append(data['budget'])

    df = pd.read_csv("./static/my_app/csv/actors_info.csv", header=0).values
    age1, amount1, gender1 = -1, -1, -1
    for row in df:
        if row[1].lower() == data['actor1'].lower():
            age1 = year - row[2]
            amount1 = row[3]
            if row[4] == 'actor':
                gender1 = 1
            else:
                gender1 = 2
            break
    vec.append(age1)
    vec.append(amount1)
    vec.append(gender1)

    age2, amount2, gender2 = -1, -1, -1
    for row in df:
        if row[1].lower() == data['actor2'].lower():
            age2 = year - row[2]
            amount2 = row[3]
            if row[4] == 'actor':
                gender2 = 1
            else:
                gender2 = 2
            break
    vec.append(age2)
    vec.append(amount2)
    vec.append(gender2)

    df = pd.read_csv("./static/my_app/csv/directors_info.csv", header=0).values
    director = data['director']
    for row in df:
        if row[1].lower() == director.lower():
            director = row[2]
            break
    vec.append(director)
    return vec


def calc_result(input_vec):
    reg = load('./static/my_app/csv/our_model.joblib')
    to_predict = create_pd(input_vec)
    y_pred = reg.predict(to_predict)[0]
    return y_pred
