from object.actor import Actor

class Film:
    def __init__(self, name=None, cast=[], producer=None, director=None, genre=[], age_rating=None, year=None, description=None):
        self.name = name
        self.cast = cast
        self.producer=producer
        self.director=director
        self.genre = genre
        self.age_rating=age_rating
        self.year = year
        self.description = description

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
        year = input("When did the file release : ").strip()
        self.year = year if year else None
    
    def prompt_genre(self):
        while True:
            genre = input("What genre is the film? : ").strip()
            if not genre:
                break
            self.genre.append(genre)

            choice = input("Add another genre? Y/N : ").strip()
            if choice.lower() != "y":
                break
    
    def prompt_cast(self):
        while True:
            actor = input("What actor is in this film? : ").strip()
            if not actor:
                break
            role = input("What is that "+actor+"'s role? : ").strip()

            self.cast.append(Actor(actor, role))

            choice = input("Add another actor? Y/N : ").strip()
            if choice.lower() == "y":
                continue
            else:
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
        choice = input("Confirm and save this film? : ").strip()
        if choice.lower() == "y":
            return True
        else:
            return False
    
    def display_film(self):
        print("film name:",self.name)
        print("Director:",self.director)
        print("Producer:",self.producer)
        print("Realse year:",self.year)
        print("Age rating:",self.age_rating)
        print("Genre:",self.genre)
        print("Cast: ")
        for actors in self.cast:
            actors.display_actor()
        print("\n")


        

        

        

        

        





            

        




