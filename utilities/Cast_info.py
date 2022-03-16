import sys

import pandas as pd

sys.path.append("..")

if __name__ == '__main__':
    # reading data sets
    actors_df = pd.read_csv("../data/original/IMDb title_principals.csv", header=0).values
    names_df = pd.read_csv("../data/original/IMDb names.csv", header=0).values

    # collect relevant data from the origin "title principals" data set
    # that only includes movies with actor/actress category which have order 1 or 2
    # each item in updated_title_principals is a "imdb_title_id,ordering, imdb_name_id,category" of a movie

    updated_title_principals = []
    for i in actors_df:
        if i[3] != 'actress' and i[3] != 'actor':
            continue
        if i[1] <= 2:
            updated_title_principals.append(list(i[j] for j in [0, 1, 2, 3]))

    # building our relevant data set
    dfPrincipals = pd.DataFrame(updated_title_principals)

    # create some dictionaries
    actor_amount_of_films = {}  # (actor -> number of movies)
    actors_gender = {}  # (actor -> gender)
    movies_top_stars = {}  # (movie -> list of two stars)
    actor_names = {}
    actor_birth = {}

    index = 0
    # iterate over the 'imdb_title_id' list and for each id/key create an empty list as value
    for i in dfPrincipals[0]:
        movies_top_stars[i] = []

    # iterate over the 'imdb_title_id' list and fill the empty lists for each id/key with stars ids
    for i in dfPrincipals[0]:
        movies_top_stars[i].append(dfPrincipals[2][index])
        index += 1

    index = 0
    # iterate over the 'imdb_name_id' list and fill the gender of each name_id, also fill zeros to the other dictionary
    for i in dfPrincipals[2]:
        actors_gender[i] = dfPrincipals[3][index]
        actor_amount_of_films[i] = 0
        index += 1

    for i in dfPrincipals[2]:
        actor_amount_of_films[i] += 1

    for row in names_df:
        actor_names[row[0]] = row[1]
        date = row[6]
        if type(date) == str:
            if date[0] == 'c' and date[3] == "1":
                actor_birth[row[0]] = date[3:7]
            elif date[0] == '1':
                actor_birth[row[0]] = date[0:4]
            else:
                actor_birth[row[0]] = float('nan')
        else:
            actor_birth[row[0]] = date

    actor_names_list = []
    for actor_id in actor_amount_of_films:
        ls = []
        ls.append(actor_id)
        ls.append(actor_names[actor_id])
        ls.append(actor_birth[actor_id])
        ls.append(actor_amount_of_films[actor_id])
        ls.append(actors_gender[actor_id])
        actor_names_list.append(ls)

    actors_ids_and_names = pd.DataFrame(actor_names_list)
    actors_ids_and_names.to_csv("../data/created/actors_info.csv",
                                header=['imdb_name_id', 'name', 'date_of_birth', 'amount of movies', 'gender'],
                                index=False)

    # csv (movie id , acotr1 id , number movies1 ,actor\actress ,..)
    final_list = []

    for i in movies_top_stars:  # i movie key
        ls = []
        ls.append(i)
        for j in movies_top_stars[i]:  # j movie value
            ls.append(j)
            ls.append(actor_birth[j])
            ls.append(int(actor_amount_of_films[j]))
            ls.append(actors_gender[j])
        final_list.append(ls)

    movies_actors = pd.DataFrame(final_list)
    movies_actors.to_csv("../data/created/movies_actors.csv",
                         header=['imdb_title_id', 'actor1_id', 'date_of_birth1', 'movies_number1', 'gender1',
                                 'actor2_id', 'date_of_birth2', 'movies_number2', 'gender2'], index=False)

    # --------------------------------------------------------------------------------------------------------------

    updated_title_principals = []
    for i in actors_df:
        if i[3] != 'director':
            continue
        if i[1] <= 10:
            updated_title_principals.append(list(i[j] for j in [0, 1, 2, 3]))

    dfPrincipals = pd.DataFrame(updated_title_principals)

    director_amount_of_films = {}  # (actor , number of movies)
    movies_director = {}  # (movies , director)
    directorId_names = {}

    index = 0
    for movie_id in dfPrincipals[0]:
        if movie_id in movies_director:
            index += 1
            continue
        movies_director[movie_id] = dfPrincipals[2][index]
        index += 1

    for director_id in dfPrincipals[2]:
        director_amount_of_films[director_id] = 0

    for director_id in dfPrincipals[2]:
        director_amount_of_films[director_id] += 1

    for row in names_df:
        directorId_names[row[0]] = row[1]

    director_names_list = []
    for director_id in director_amount_of_films:
        ls = []
        ls.append(director_id)
        ls.append(directorId_names[director_id])
        ls.append(director_amount_of_films[director_id])
        director_names_list.append(ls)

    directors_ids_and_names = pd.DataFrame(director_names_list)
    directors_ids_and_names.to_csv("../data/created/directors_info.csv",
                                   header=['imdb_name_id', 'name', 'amount of movies'],
                                   index=False)

    # csv (movie id , acotr1 id , number movies1 ,actor\actress ,..)
    final_list = []
    for m_id in movies_director:  # m_id movie key
        ls = []
        ls.append(m_id)
        d_id = movies_director[m_id]
        ls.append(d_id)
        ls.append(director_amount_of_films[d_id])
        final_list.append(ls)

    movies_directors = pd.DataFrame(final_list)
    movies_directors.to_csv("../data/created/movies_directors.csv",
                            header=['imdb_title_id', 'director_id', 'movies_number'], index=False)
