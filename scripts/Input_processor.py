import sys

sys.path.append("..")

import pandas as pd
from joblib import load
from utilities.Normalization import *
from utilities.Split import *

# from sklearn.ensemble import GradientBoostingRegressor

genres_list = ['adult', 'action', 'adventure', 'animation', 'biography', 'comedy', 'crime', 'documentary', 'drama',
               'family', 'fantasy', 'film-noir', 'history', 'horror', 'music', 'musical', 'mystery', 'romance',
               'sci-fi', 'sport', 'thriller', 'war', 'western']


def take_input():
    word = input()
    if word == 'quit':
        sys.exit()
    return word


def set_year():
    print("To start, please enter the production year of your movie:")
    year = take_input()
    while not year.isnumeric():
        print("Your input is invalid, please type a number!")
        year = take_input()
    return int(year)


def set_month():
    print("Please enter the month (in numbers) when the movie was published:")
    month = take_input()
    while not month.isnumeric() or int(month) < 1 or int(month) > 12:
        print("Your input is invalid, please type a correct month number!")
        month = take_input()
    return int(month)


def set_genre():
    genre = take_input()
    while not genre.isalpha() or genre.lower() not in genres_list:
        print("Your input is invalid, try again!")
        print("If you wish to display all the genres that our program supports, please type the word 'show'.")
        genre = take_input()
        if genre == 'show':
            for g in genres_list:
                print(g)
            print()
            print("Please try again:")
            genre = take_input()
    return genre


def set_genres():
    print("Please enter a genre to your movie:")
    genre_lst = []
    genre_lst.append(set_genre().lower())
    count = 1
    while count < 3:
        print("If you wish to add another genre, please type 'add', else type 'continue'.")
        answer = take_input()
        if answer == 'add':
            print("Add another genre:")
            genre_lst.append(set_genre().lower())
            count += 1
        elif answer == "continue":
            break
        else:
            print("Your input is invalid, try again!")
    genre_lst = sorted(genre_lst, key=str.lower)
    genres = (' '.join(genre_lst))
    df = pd.read_csv("../data/created/Genres.csv", header=0).values
    for row in df:
        if row[0] == genres:
            genres = row[1]
            break
    return genres


def set_duration():
    print("Please enter the duration of the movie (in minutes):")
    duration = take_input()
    while not duration.isnumeric():
        print("Your input is invalid, please type a number!")
        duration = take_input()
    return int(duration)


def set_country():
    df = pd.read_csv("../data/created/Countries.csv", header=0)
    countries = list(df['country'])
    country = take_input()
    while not country.isalpha() or country.lower() not in countries:
        print("Your input is invalid, try again!")
        print("If you wish to display all the countries that our program supports, please type the word 'show'.")
        country = take_input()
        if country == 'show':
            for c in countries:
                print(c)
            print()
            print("Please try again:")
            country = take_input()
    return country


def set_countries():
    df = pd.read_csv("../data/created/Countries.csv", header=0).values
    print("Please enter the main production country:")
    country1 = set_country().lower()
    for row in df:
        if row[0] == country1:
            country1 = row[1]
            break

    print("If you wish to add another country, please type 'add', else type 'continue'.")
    while True:
        answer = take_input()
        if answer == 'add':
            print("Please enter the second main production country:")
            country2 = set_country().lower()
            for row in df:
                if row[0] == country2:
                    country2 = row[1]
                    return country1, country2
        elif answer == "continue":
            return country1, -1
        else:
            print("Your input is invalid, try again!")


def set_languege():
    df = pd.read_csv("../data/created/Languages.csv", header=0)
    languages = list(df['languages'])
    language = take_input()
    while not language.isalpha() or language.lower() not in languages:
        print("Your input is invalid, try again!")
        print("If you wish to display all the languages that our program supports, please type the word 'show'.")
        language = take_input()
        if language == 'show':
            for l in languages:
                print(l)
            print()
            print("Please try again:")
            language = take_input()
    return language


def set_languages():
    df = pd.read_csv("../data/created/Languages.csv", header=0).values
    print("Please enter the main language spoken in the movie:")
    language1 = set_languege().lower()
    for row in df:
        if row[0] == language1:
            language1 = row[1]
            break

    print("If you wish to add another language, please type 'add', else type 'continue'.")
    while True:
        answer = take_input()
        if answer == 'add':
            print("Please enter the second main language spoken in the movie:")
            language2 = set_languege().lower()
            for row in df:
                if row[0] == language2:
                    language2 = row[1]
                    return language1, language2
        elif answer == "continue":
            return language1, -1
        else:
            print("Your input is invalid, try again!")


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


def set_production_company():
    df = pd.read_csv("../data/created/Productions.csv", header=0).values
    productions = [row[0] for row in df]
    # print(productions)
    print("Please enter the name of the production company:")
    production = take_input()
    production = production.lower()
    isSubString = False
    for i in productions:
        if production in correct_production_company(i).lower():
            isSubString = True
            break
    while not isSubString:
        print("Your input is invalid, please try again!")
        print(
            "If you wish to display some examples of production companies that our program supports, please type the word 'show'.")
        production = take_input()
        production = production.lower()
        if production == 'show':
            for p in productions[:15]:
                print(p)
            print()
            print("Please try again:")
            production = take_input()
            production = production.lower()
            isSubString = False
            for i in productions:
                if production in correct_production_company(i).lower():
                    isSubString = True
                    break
    for row in df:
        if production.lower() in correct_production_company(row[0]).lower():
            return row[1]


def set_budget():
    print("Please enter the budget of the movie (in dollars) :")
    budget = take_input()
    while not budget.isnumeric():
        print("Your input is invalid, please type a number!")
        budget = take_input()
    return int(budget)


def set_actor():
    df = pd.read_csv("../data/created/actors_info.csv", header=0)
    actors_names = list(df['name'])
    actors_names = [a.lower() for a in actors_names]
    some_actors = actors_names[:15]
    actor = take_input()
    while actor.lower() not in actors_names:
        print("Your input is invalid, try again!")
        print("If you wish to display *some* actors names that our program supports, please type the word 'show'.")
        actor = take_input()
        if actor == 'show':
            for a in some_actors:
                print(a)
            print()
            print("Please try again:")
            actor = take_input()
    return actor


def set_actors_info(year):
    df = pd.read_csv("../data/created/actors_info.csv", header=0).values
    print("Please enter two movie actors names:")
    print("Enter first actor:")
    actor1 = set_actor().lower()
    age1, amount1, gender1 = -1, -1, -1
    for row in df:
        if row[1].lower() == actor1:
            age1 = year - row[2]
            amount1 = row[3]
            if row[4] == 'actor':
                gender1 = 1
            else:
                gender1 = 2
            break
    print("Enter second actor:")
    age2, amount2, gender2 = -1, -1, -1
    actor2 = set_actor().lower()
    for row in df:
        if row[1].lower() == actor2:
            age2 = year - row[2]
            amount2 = row[3]
            if row[4] == 'actor':
                gender2 = 1
            else:
                gender2 = 2
    return age1, amount1, gender1, age2, amount2, gender2


def set_director():
    df = pd.read_csv("../data/created/directors_info.csv", header=0).values
    directors = [i[1].lower() for i in df]
    # print(directors)
    print("Please enter the director of the movie:")
    director = take_input().lower()
    while director.lower() not in directors:
        print("Your input is invalid, try again!")
        print("If you wish to display *some* directors names that our program supports, please type the word 'show'.")
        director = take_input()
        if director == 'show':
            for a in directors[:15]:
                print(a)
            print()
            print("Please try again:")
            director = take_input()
    for row in df:
        if row[1].lower() == director:
            director = row[2]
            break
    return int(director)


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


if __name__ == '__main__':
    df = pd.read_csv("../data/created/Main_data.csv", header=0)
    input_vec = []
    print("We Are Glad To Help You Predict Your Movie Rating!")
    print("If you decide to end the process, please type the word 'quit'.")

    year = set_year()
    input_vec.append(year)
    input_vec.append(set_month())
    input_vec.append(set_genres())
    input_vec.append(set_duration())

    country1, country2 = set_countries()
    input_vec.append(country1)
    input_vec.append(country2)
    if country2 == -1:
        input_vec.append(0)
    else:
        input_vec.append(1)

    language1, language2 = set_languages()
    input_vec.append(language1)
    input_vec.append(language2)
    if language2 == -1:
        input_vec.append(0)
    else:
        input_vec.append(1)

    input_vec.append(set_production_company())
    input_vec.append(set_budget())

    age1, amount1, gender1, age2, amount2, gender2 = set_actors_info(year)
    input_vec.append(age1)
    input_vec.append(amount1)
    input_vec.append(gender1)
    input_vec.append(age2)
    input_vec.append(amount2)
    input_vec.append(gender2)
    input_vec.append(set_director())

    print(input_vec)
    print("It might take a while, please wait :) ...")
    reg = load('our_model.joblib')

    #--------------------------------------------------------------------------------
# [year , month , genres , duration , country1 ,country2 ,  isSecond , languege1 , languge2 , isSecond , company , budegt,
#  age1 , amount1 , gender1 ,age2,amount2,gender2,directoramount]
#     godfather = [1972 , 9 , 1231 ,175,1,-1,0,1,9,1,4 ,6000000,48,33,1,32,42,1,27] # 9.2 8.6
#     memento  = [2000, 1, 2000, 113, 1, -1, 0, 1, -1, 0, 2314, 9000000, 33.0, 29, 1, 33.0, 10, 2, 11]
#     titanic = [1997, 1, 1557, 194, 1, 17, 1, 1, 12, 1, 5, 200000000, 23.0, 23, 1, 22.0, 28, 2, 8] # 7.8 7.1

    #--------------------------------------------------------------------------------


    # g = create_pd(godfather)
    # m = create_pd(memento)
    # t = create_pd(titanic)
    to_predict = create_pd(input_vec)

    X_train, X_test, orig_y_train, y_test = split_one_train_one_test(df)
    X_train, X_test, y_train, y_test = normalize(X_train, to_predict, orig_y_train, [])

    #X_train, X_test, y_train, y_test = normalize(X_train, to_predict, orig_y_train, [])

    y_pred = reg.predict(X_test)[0]
    final_result = reverse_normalization(y_pred, orig_y_train)
    print()
    print('THE PREDICTED RATING OF YOUR MOVIE IS:', final_result)

    # GB_best_reg = GradientBoostingRegressor(max_depth=5, n_estimators=400)
    # input_vec = [1997, 1, 1557, 194, 1, 17, 1, 1, 12, 1, 5, 200000000, 23, 23, 1, 22, 28, 2, 8]
    # to_predict = create_pd(input_vec)
    #
    # X_train, X_test, orig_y_train, y_test = split_one_train_one_test(df)
    # X_train, X_test, y_train, y_test = normalize(X_train, to_predict, orig_y_train, [])
    #
    # reg.fit(X_train, y_train)
    # y_pred = reg.predict(X_test)[0]
    # final_result = reverse_normalization(y_pred, orig_y_train)
    # print(final_result)
