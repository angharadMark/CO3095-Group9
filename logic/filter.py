import operator
import functools
import itertools

from object.filter_type import FilterType
from object.film import Film

def string_fuzzy_match(one : str, two : str):
    if (type(one) != str and type(one) != bytes) or (type(two) != str and type(two) != bytes): return False
    return one.strip().lower() == two.strip().lower()

class QueryFilter:
    def __init__(self, type : FilterType, content : str):
        self.type = type
        self.content = content

    def get_type(self) -> FilterType: return self.type
    def get_content(self) -> str: return self.content
    def matches(self, film : Film) -> bool:
        if not issubclass(type(film), Film): return False
        if self.type == FilterType.CAST:
            return functools.reduce(lambda a, b: a or b, 
                map(lambda actor: string_fuzzy_match(actor.name, self.content), film.cast),
                False
            )
        elif self.type == FilterType.GENRE:
            if type(film.genre) == list:
                return functools.reduce(lambda a, b: a or b, 
                    map(lambda genre: string_fuzzy_match(genre, self.content), film.genre),
                    False
                )
            else:
                return string_fuzzy_match(film.genre, self.content)
        return False

def filter_films(filter_list : list[QueryFilter], films : list[Film]) -> list[Film]:
    if type(films) != list or type(filter_list) != list: return []
    if len(filter_list) == 0: return films
    if len(films) == 0: return []
    return [film for film in films if functools.reduce(lambda a, b: a or b,
        map(lambda filter: filter.matches(film), filter_list)
    )] 
