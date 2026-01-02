from logic.user_registration import readJson, saveJson, usersFile

from collections import Counter

class WatchlistSimilarity:
    @staticmethod
    def get_watchlist_genres(watchlist):
        return [genre for film in watchlist for genre in film.genre]

    # returns all users that have a similar watchlist to target_user ranked by
    # a similarity score
    @staticmethod
    def find(target_user, database):
        users_json_data = readJson(usersFile, {"byId":{}, "byUsername": {}})

        (target_user_data, target_user_id) = target_user.get_user_data(users_json_data)

        similarities = []

        target_film_genres = WatchlistSimilarity.get_watchlist_genres(target_user.watchList)
        counted_target_genres = dict(Counter(target_film_genres))

        for (user_id, user_data) in users_json_data["byId"].items():
            if user_id == target_user_id: continue
            user_name = user_data["username"]

            similarity_score = 0
   
            retrieved_films = [] if "watchList" not in user_data.keys() else [database.get_film(film) for film in user_data["watchList"]]

            # direct similarity
            for film in target_user.watchList:
                if film in retrieved_films:
                    similarity_score += 20
            
            # indirect similarity (by genre)
            film_genres = WatchlistSimilarity.get_watchlist_genres(retrieved_films)
            counted_genres = dict(Counter(film_genres))

            for (target_film_genre, target_occurence) in counted_target_genres.items():
                if target_film_genre not in counted_genres: continue

                other_occurence = counted_genres[target_film_genre]

                # added similarity score = (other_user_genre_occurrence) / target_user_genre_occurence
                similarity_score += (other_occurence / target_occurence)

            similarities.append((user_name, similarity_score))

        similarities = [(user_name, similarity_score) for (user_name, similarity_score) in similarities if similarity_score > 0]

        return sorted(similarities, key= lambda similarity_tuple : similarity_tuple[1], reverse=True)


