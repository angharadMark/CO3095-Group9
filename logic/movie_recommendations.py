import random
from database.database_loader import DatabaseLoader

def getMovieOfTheDay(fileName="films.json"):
    loader=DatabaseLoader()
    database=loader.load(fileName)

    all_films=database.get_all_films()
    if not all_films:
        return None

    movie=random.choice(all_films)
    return movie

def similarity_results(film_1, film_2):
    similarity_points = 0

    for genre_1 in film_1.get_genre():
        for genre_2 in film_2.get_genre():
            if genre_1 == genre_2:
                similarity_points+=2
    

    for actors_1 in film_1.cast:
        for actors_2 in film_2.cast:
            if actors_1.name == actors_2.name:
                similarity_points+=1
    

    if film_1.director == film_2.director:
        similarity_points+=1


    if film_1.producer == film_2.producer:
        similarity_points+=1

    return similarity_points

#manual testing commented out
"""
def similarity_results(film_1, film_2):
    similarity_points = 0
    print("TESTING")

    for genre_1 in film_1.get_genre():
        for genre_2 in film_2.get_genre():
            if genre_1 == genre_2:
                similarity_points += 2
                print(similarity_points)
                print(genre_1, genre_2)


    for actors_1 in film_1.cast:
        for actors_2 in film_2.cast:
            if actors_1.name == actors_2.name:
                similarity_points += 1
                print(similarity_points)
                print(actors_1.name, actors_2.name)


    if film_1.director == film_2.director:
        similarity_points += 1
        print(similarity_points)
        print(film_1.director, film_2.director)


    if film_1.producer == film_2.producer:
        similarity_points += 1
        print(similarity_points)
        print(film_1.producer, film_2.producer)

    print(similarity_points)
    print("END TEST")
    return similarity_points
"""
def reccomend_films(user, database, limit = 5):
    reccomendation = []
    watchlist_names = [film.name for film in user.get_watch_list()]
    
    if not watchlist_names:
        print("Your watchlist is currently empty!")
        return []
    
    for film in database.get_all_films():
        if film.name in watchlist_names:
            continue
        
        total_score = 0
        for watchlist_film in user.get_watch_list():
            total_score += similarity_results(film, watchlist_film)

        if total_score > 4:
            reccomendation.append((film, total_score))

    reccomendation.sort(reverse=True, key=lambda x: x[1])

    # Return only films, up to limit
    return [film for film, score in reccomendation[:limit]]