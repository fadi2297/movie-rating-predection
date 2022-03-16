import itertools

import pandas as pd


def generate_combinations(types, size):
    ls1, ls = [], []
    for i in range(size):
        ls.extend(list(itertools.combinations(types, i + 1)))
    for i in ls:
        ls1.append(list(i))
    for i in ls1:
        i.sort()
    ls2 = []
    ls1.sort()
    for i in ls1:
        ls2.append(" ".join(i))
    return ls2


if __name__ == '__main__':
    # movies genres
    genres_list = ['adult', 'action', 'adventure', 'animation', 'biography', 'comedy', 'crime', 'documentary', 'drama',
                   'family', 'fantasy', 'film-noir', 'history', 'horror', 'music', 'musical', 'mystery', 'romance',
                   'sci-fi', 'sport', 'thriller', 'war', 'western']

    ls = generate_combinations(genres_list, 3)
    df1 = pd.DataFrame({'genre': ls, 'number': range(len(ls))})
    df1.to_csv("../data/created/Genres.csv", index=False)

    df = pd.read_csv("../data/original/IMDb movies.csv", header=0).values
    production_dict = {}
    for row in df:
        company = row[11]
        if type(company) == str:
            production_dict[company.lower()] = 0

    for row in df:
        company = row[11]
        if type(company) == str:
            production_dict[company.lower()] += 1

    sorted_dict = dict(sorted(production_dict.items(), key=lambda item: -item[1]))
    names_list = []
    amount_list = []
    numbers = []
    count = 1
    for company in sorted_dict:
        names_list.append(company)
        amount_list.append(sorted_dict[company])
        numbers.append(count)
        count += 1

    df1 = pd.DataFrame({'production company': names_list, 'order': numbers, 'number of movies': amount_list})
    df1.to_csv("../data/created/Productions.csv", index=False)

    df = pd.read_csv("../data/original/countries_ordered_by_grossing.csv", header=0).values
    countries_list = [row[0].lower() for row in df]
    df1 = pd.DataFrame({'country': countries_list, 'number': range(1, len(countries_list) + 1)})
    df1.to_csv("../data/created/Countries.csv", index=False)

    df = pd.read_csv("../data/original/languages_ordered_by_grossing.csv", header=0).values
    languages_list = ['none']
    languages_list = languages_list + [row[0] for row in df]
    df1 = pd.DataFrame({'languages': languages_list, 'number': range(0, len(languages_list))})
    df1.to_csv("../data/created/Languages.csv", index=False)
