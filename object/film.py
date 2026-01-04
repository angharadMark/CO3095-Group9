from object.actor import Actor

from copy import deepcopy

class Film:
    def __init__(self, name=None, cast=None, producer=None, director=None, genre=None, age_rating=None, year=None, ratings=None, description=None, comments=None):
        self.name = name
        self.cast = cast if cast is not None else []
        self.producer=producer
        self.director=director
        self.genre = genre if genre is not None else []
        self.age_rating=age_rating
        self.year = year
        self.ratings = ratings if ratings is not None else []
        self.description = description
        self.comments = comments if comments  is not None else []

    def to_dict(self):
        return{
            "name": self.name,
            "director": self.director,
            "producer": self.producer,
            "year": self.year,
            "genre": self.genre,
            "ratings": self.ratings,
            "cast": [{
                "actor": actor.name,
                "role": actor.role
                }
                for actor in self.cast
            ],
            "comments": [
                {
                    "user": comment.user,
                    "message": comment.message  
                }
                for comment in self.comments
            ],
            "age_rating": self.age_rating,
            "description": self.description
        }
    
    def add_actor(self, actor):
        for a in self.cast:
            if a.name == actor.name and a.role == actor.role:
                return False
        self.cast.append(actor)
        return True

    def prompt_name(self):
        name = input("Whats the name of the film? : ").strip()
        self.name = name if name else None

    def prompt_producer(self):
        producer = input("Whats the producer of the film? : ").strip()
        self.producer = producer if producer else None
    
    def prompt_director(self):
        director = input("Whats the director of the film? : ").strip()
        self.director = director if director else None
    
    def prompt_age_rating(self):
        age_rating = input("Whats the age rating of the film? : ").strip()
        self.age_rating = age_rating if age_rating else None
    
    def prompt_year(self):
        while True:
            year = input("When did the film release : ").strip()
            if not year:
                self.year = None
                return
            if year.isdigit():
                self.year = int(year)
                return
            print("Please input a valid year.")
    
    def prompt_genre(self):
        first_run = True

        while True:
            genre = input("What genre is the film? : ").strip()
            if not genre:
                break
            if first_run:
                self.genre = []
            first_run = False

            genre = genre.title()

            if genre not in self.genre:
                self.genre.append(genre)
            else:
                print("Genre already added!")

            self.genre.append(genre)

            choice = input("Add another genre? Y/N : ").strip()
            if choice.lower() != "y":
                break
    
    def prompt_cast(self):
        first_run = True

        while True:
            actor = input("What actor is in this film? : ").strip()
            if not actor:
                break
            if first_run:
                self.cast = []
            first_run = False
            role = input("What is that "+actor+"'s role? : ").strip().title()

            actor_obj = Actor(actor.title(), role)
            added = self.add_actor(actor_obj)

            if added == False:
                print("Actor already added to this film!")
                continue
            else:
                print(f"{actor.title()} has been added!")

            choice = input("Add another actor? Y/N : ").strip().lower()
            if choice.lower() != "y":
                break


    def input_film(self):
        print("Please enter the details of the film, Press enter to skip ")
        self.prompt_name()
        self.prompt_producer()
        self.prompt_director()
        self.prompt_year()
        self.prompt_age_rating()
        self.prompt_genre()
        self.prompt_cast()

        self.display_film()
        choice = input("Confirm and save this film? y/n : ").strip()
        if choice.lower() == "y":
            return True
        else:
            return False

    def modify_film(self):
        temp_film = deepcopy(self)

        if temp_film.input_film():
            if temp_film.get_name() != None:
                self.set_name(temp_film.get_name())
            if temp_film.get_producer() != None:
                self.set_producer(temp_film.get_producer())
            if temp_film.get_director() != None:
                self.set_director(temp_film.get_director())
            if temp_film.get_year() != None:
                self.set_year(temp_film.get_year())
            if temp_film.get_age_rating() != None:
                self.set_age_rating(temp_film.get_age_rating())
            if temp_film.get_genre() != None:
                self.set_genre(temp_film.get_genre())
            if temp_film.get_cast() != None:
                self.set_cast(temp_film.get_cast())

            self.display_film()
            return True

        return False
    
    def average_rating(self):
        average = 0
        if not self.ratings:
            return 0
        else:
            for rating in self.ratings:
                average += rating 
            average = average / len(self.ratings)
            return round(average,2)
    
    def display_film(self):
        print("\n")
        print("film name:",self.name)
        print("Director:",self.director)
        print("Producer:",self.producer)
        print("Release year:",self.year)
        print("Age rating:",self.age_rating)
        print("Genre:",self.genre)
        print("Cast: ")
        for actors in self.cast:
            actors.display_actor()
            print("\n")
        if self.average_rating() == 0:
            print("unrated")
        else:
            print("Average rating: "+ str(self.average_rating()))
        print("Comments: ")
        for comment in self.comments:
            comment.display_comment()
        print("\n")
    
    def add_ratings(self, rating):
        self.ratings.append(rating)
            
    def add_comment(self, comment):
        self.comments.append(comment)

    def get_name(self): 
        return self.name

    def get_producer(self):
        return self.producer

    def get_director(self):
        return self.director

    def get_year(self):
        return self.year

    def get_age_rating(self):
        return self.age_rating

    def get_genre(self):
        return self.genre

    def get_cast(self):
        return self.cast

    def set_name(self, name):
        self.name = name
        
    def set_producer(self, producer):
        self.producer = producer

    def set_director(self, director):
        self.director = director

    def set_year(self, year):
        self.year = year

    def set_age_rating(self, age_rating):
        self.age_rating = age_rating

    def set_genre(self, genre):
        self.genre = genre if genre is not None else []

    def set_cast(self, cast):
        self.cast = cast if cast is not None else []

def searchMovies(movies, keyword):
    keyword = keyword.lower().strip()
    results = []

    for movie in movies:
        title = (movie.name or "").lower()
        description = (getattr(movie, 'description', "") or "").lower()

        if keyword in title or keyword in description:
            results.append(movie)
    
    return results

