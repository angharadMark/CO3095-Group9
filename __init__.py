import argparse
import itertools

from logic.filter import *
from object.filter_type import FilterType
from database.database_loader import DatabaseLoader

def process_filter(values, filter_enum):
    tied_filters = list(zip(values, [filter_enum] * len(values)))

    return [QueryFilter(filter_type, text) for (text, filter_type) in tied_filters]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="FilmDatabase")

    # Move database loading inside so it doesn't slow down tests
    database = DatabaseLoader().load("films.json")

    parser.add_argument("-fc", "--filter-cast", nargs="+", default=[])
    parser.add_argument("-fg", "--filter-genre", nargs="+", default=[])

    args = vars(parser.parse_args())

    filters = [
        ("filter_cast", FilterType.CAST),
        ("filter_genre", FilterType.GENRE)
    ]

    retrieved_filters = list(itertools.chain(
        *map(lambda values: process_filter(args[values[0]], values[1]), filters))
    )

    film_list = filter_films(retrieved_filters, database.get_all_films())

    if len(film_list) > 0:
        print("Matched films: ")
        for film in film_list:
            print(film.name)