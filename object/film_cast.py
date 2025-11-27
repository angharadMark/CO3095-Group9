class FilmCast:
    def __init__(self, film):
        self.film=film
        self.cast=[]

    def add_whole_cast(self,cast):
        for actor in cast:
            self.cast.append(actor)
    
    def add_actor(self, actor):
        self.cast.append(actor)
