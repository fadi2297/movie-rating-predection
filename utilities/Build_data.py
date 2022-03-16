import math
import sys

sys.path.append("..")
import pandas as pd

# those are the features we extract for each movie and create a data set for them.
# each movie is representd as a vector of selected features below

selected_features = ['year', 'month', 'genre', 'duration', 'first country', 'second country', 'Is second country',
                     'first language', 'second language', 'Is second language', 'production company', 'budget',
                     'first actor age', 'first actor amount of movies', 'first actor gender', 'second actor age',
                     'second actor amount of movies', 'second actor gender', 'director amount of movies']


# func: params:row : row of features
#      output: year of the movie in the row (returned as integer) , float(nan) if year is missing
def extract_year(row):
    year = str(row[3])
    if not year.isnumeric():
        return float('nan')
    return int(year)


# func:  params:row : row of features
#      output: published month of the movie in the row extracted from the date_published(returned as integer) ,
#      float(nan) if date is missing
def extract_month(row):
    if len(row[4]) < 10:
        return float('nan')
    else:
        month = row[4][5] + row[4][6]
        if month.isnumeric():
            return int(month)
    return float('nan')


# func: params: row : row of features
#               df : (production company,order,number of movies) data set
#      output: order of the production company that appears in the row,
#      float(nan) if production company does not appear in the data set df
def extract_company(row, df):
    production = row[11]
    if type(production) != str:
        return production
    for r in df:
        if r[0] == production.lower():
            return r[1]
    return float('nan')


# func: params: row : row of features
#               df : (cuurency,value in dollar) data set
#      output: budget in dollars
#      float(nan) if currency does not appear in the data set df
def extract_budget(row, df):
    budget = row[16]
    if type(budget) != str:
        return budget
    budget_splitted = budget.split(" ")
    # budget in dollars then return it
    if budget_splitted[0] == '$':
        return float(budget_splitted[1])
    # budget isnt in dollars, find the currency value in dollar and return budget in dollars
    for r in df:
        if r[0] == budget_splitted[0]:
            return float(r[1]) * float(budget_splitted[1])
    return float('nan')


# this function splits multiple countries/multiple languages to two different lists first and second then returns it
# as output.
# params: info_df: languages or countries data set represented with numbers (lnaguage/country , number)
#         df : big data, movies as vectors of features
#          n : column/number of feature wich we want to iterate on
#          output : two different lists of countries/languages
def extract_lists(info_df, df, n):
    info = [row[n] for row in df]  # list of strings
    info_list_of_lists = []
    # iterate over the info list which can include languages or countries of movies
    # item : languages or countries of the iteration specific movie
    for item in info:
        if type(item) != str:
            info_list_of_lists.append([])
            continue
        current = item.lower().split(", ")  # split item
        info_list_of_lists.append(current)
    first_info = []  # includes the most important value in the item
    second_info = []  # includes the second most important value in the item
    counter = 0
    for lst in info_list_of_lists:
        if lst == []:  # lst has empty info
            first_info.append(float('nan'))
            second_info.append(float('nan'))
        elif len(lst) == 1:  # lst has exactly one coutnry/language info
            for r in info_df:
                if r[0] == lst[0]:
                    first_info.append(r[1])
                    second_info.append(-1)  # represents a null country
                    break
        else:
            for r in info_df:
                if r[0] == lst[0]:
                    first_info.append(r[1])
                    break
            for r in info_df:
                if r[0] == lst[1]:
                    second_info.append(r[1])
                    break
        if len(first_info) != counter + 1:
            first_info.append(float('nan'))
        if len(second_info) != counter + 1:
            second_info.append(float('nan'))
        counter += 1

    return first_info, second_info


# func: params: row : row of features
#               genres_df : (combination of at most 3 genres , number) data set
#      output: the order number of the genres combination which appears in the row,
#      float(nan) if genres combination does not appear in the data set
def extract_genre(genres_df, row):
    genre = row[5]
    if type(genre) != str:
        return genre
    genre = genre.lower()
    genre = genre.split(", ")
    genre_words = sorted(genre, key=str.lower)
    genre = (' '.join(genre_words))
    for g in genres_df:  # find the genre in the data set
        if genre == g[0]:
            return g[1]  # return its order number
    # genre does not appear
    return float('nan')


# func: params: birth years : list of stars birth years
#              years_list : list of movies published years
#      output: list of stars ages when they playes their movies,
#      float(nan) appended to output list if there is missing info

def extract_age(birth_years, years_list):
    ls = []
    for i in range(len(birth_years)):
        if not math.isnan(birth_years[i]) and not math.isnan(years_list[i]):
            ls.append((years_list[i]) - int(birth_years[i]))
        else:
            ls.append(float('nan'))
    return ls


# func: params: row : a specific person gender
#
#      output: "actor" or "actress" gender ,
#      float(nan) in error case
def extract_gender(row):
    gender = row
    if gender == 'actor':
        return 1
    if gender == 'actress':
        return 2
    return float('nan')


def get_second(second_lst):
    IsSecondCountry = []
    for c in second_lst:
        if c == -1:
            IsSecondCountry.append(0)
        elif c == float('nan'):
            IsSecondCountry.append(float('nan'))
        else:
            IsSecondCountry.append(1)
    return IsSecondCountry


if __name__ == '__main__':
    print('Loading Data ...')
    df = pd.read_csv("../data/original/IMDb movies.csv", header=0).values

    print('Extract Years...')
    years_list = [extract_year(row) for row in df]
    print('Done:)')

    print('Extract Months...')
    months_list = [extract_month(row) for row in df]
    print('Done:)')

    print('Extract Genres...')
    genres_df = pd.read_csv("../data/created/Genres.csv", header=0).values
    genres_list = [extract_genre(genres_df, row) for row in df]
    print('Done:)')

    print('Extract Durations...')
    durations_list = [row[6] for row in df]
    print('Done:)')

    print('Extract Countires...')
    countries_df = pd.read_csv("../data/created/Countries.csv", header=0).values
    first_countries, second_countries = extract_lists(countries_df, df, 7)
    print('Done:)')

    print('Extract Languages...')
    languages_df = pd.read_csv("../data/created/Languages.csv", header=0).values
    first_languages, second_languages = extract_lists(languages_df, df, 8)
    print('Done:)')

    print('Extract Production Companies...')
    print('it takes a while...')
    productions_df = pd.read_csv("../data/created/Productions.csv", header=0).values
    production_list = [extract_company(row, productions_df) for row in df]
    print('Done:)')

    # print('Extract Budgets...')
    # budget_df = pd.read_csv("../data/original/Currencies.csv", header=0).values
    # budgets_list = [extract_budget(row, budget_df) for row in df]
    # print('Done:)')

    print("Extract Movie Countries Number...")
    IsSecondCountry = get_second(second_countries)
    print('Done')

    print("Extract Movie languages Number...")
    IsSecondLangugae = get_second(second_languages)
    print('Done')

    print('Extract Actors Info...')
    df = pd.read_csv("../data/original/IMDb movies.csv", header=0)
    df1 = pd.read_csv("../data/created/movies_actors.csv", header=0)
    df2 = pd.read_csv("../data/created/movies_directors.csv", header=0)
    merged_df = df.merge(df1, on='imdb_title_id', how='left')
    merged_twice_df = merged_df.merge(df2, on='imdb_title_id', how='left')

    actors_ages1 = extract_age(merged_df['date_of_birth1'], years_list)
    actor_amount_of_films1 = list(merged_df['movies_number1'])
    actor_gender1 = [extract_gender(row) for row in merged_df['gender1']]

    actors_ages2 = extract_age(merged_df['date_of_birth2'], years_list)
    actor_amount_of_films2 = list(merged_df['movies_number2'])
    actor_gender2 = [extract_gender(row) for row in merged_df['gender2']]
    print('Done:)')

    print('Extract Director Info...')
    director_amount_of_films = list(merged_twice_df['movies_number'])
    print('Done:)')

    rating_list = list(merged_df['avg_vote'])

    # create Data Set with information we collected/create above
    final_df = pd.DataFrame({'year': years_list,
                           'month': months_list,
                           'genre': genres_list, 'duration': durations_list,
                           'first country': first_countries, 'second country': second_countries,
                           'Is second country': IsSecondCountry,
                           'first language': first_languages, 'second language': second_languages,
                           'Is second language': IsSecondLangugae,
                           'production company': production_list,
                         #  'budget': budgets_list,
                           'first actor age': actors_ages1, 'first actor amount of movies': actor_amount_of_films1,
                           'first actor gender': actor_gender1, 'second actor age': actors_ages2,
                           'second actor amount of movies': actor_amount_of_films2,
                           'second actor gender': actor_gender2, 'director amount of movies': director_amount_of_films,
                           'average rating': rating_list
                           })

    final_df = final_df.dropna()  # drop unnecessary rows
    final_df.to_csv("../data/created/Main_data.csv", index=False)
#     final_df.to_csv("../data/created/tmp_data.csv", index=False)
