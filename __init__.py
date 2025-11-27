import argparse
import itertools

from object.filter_type import FilterType

def process_filter(values, filter_enum):
    return list(zip(values, [filter_enum] * len(values)))

parser = argparse.ArgumentParser(
    prog="FilmDatabase"
)

parser.add_argument("-fc", "--filter-cast", nargs="+", default=[])
parser.add_argument("-fg", "--filter-genre", nargs="+", default=[])

filters = [
    ("filter_cast", FilterType.CAST), 
    ("filter_genre", FilterType.GENRE)
]

args = vars(parser.parse_args())

retrieved_filters = list(itertools.chain(
    map(lambda values: process_filter(args[values[0]], values[1]), filters)
))

print(process_filter(args["filter_genre"], FilterType.GENRE))
