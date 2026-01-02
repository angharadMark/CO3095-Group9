from object.film import Film
from copy import deepcopy
from logic.user_registration import readJson, saveJson, usersFile

class User:
    def __init__(self, record, database=None, avatar_index=0,favFilm="None Set"):
        self.id = record["id"]
        self.username = record["username"]
        if database != None:
            self.watchList= [database.get_film(f) for f in record.get("watchlist",[])]
            self.dislikes = [database.get_film(film_title) for film_title in record.get("dislikes", [])]
        else:
            self.watchList = []
            self.dislikes = []

        self.films_added= record.get("films_added", 0)
        # A dictionary associating film names with their ratings (0-10)
        self.ratings = record.get("ratings", {})
        self.comments = record.get("comments", {})
        self.avatar_index = record.get("avatarIndex", avatar_index)
        self.favFilm= record.get("favFilm", favFilm)

        #Set ASCII based on the index above from database
        if 0 <= self.avatar_index < len(User.AVATAR_OPTIONS):
            self.avatar_ascii = User.AVATAR_OPTIONS[self.avatar_index]
        else:
            self.avatar_ascii = User.AVATAR_OPTIONS[0] # Fallback
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "watchlist": [film.name for film in self.watchList],
            "films_added": self.films_added,
            "ratings": self.ratings,
            "comments": [{
                "user": comment.user,
                "message": comment.message
                }
                for comment in self.comments
            ],
            "avatar_index": self.avatar_index,
            "favFilm": self.favFilm,
            "friends": [],
            "blocked": [],
            "dislikes": [film.name for film in self.dislikes]
        }
    AVATAR_OPTIONS=[
        # Got these from https://www.asciiart.eu
        # Option 1: Neutral Face
        (
            "   /\\ \n"
            "  /  \\ \n"
            " |o  o|\n"
            "  \\ - /\n"
            "   \\_/\n"
        ),
        # Option 2: MONKEY!!
        (
            "                 __------__\n"
            "              /~          ~\\\n"
            "             |    //^\\\\//^\\|\n"
            "           /~~\  ||  o| |o|:~\\\n"
            "          | |6   ||___|_|_||:|\n"
            "           \\__.  /      o  \\/'\n"
            "            |   (       O   )\n"
            "   /~~~\\    `\\  \\         /\n"
            "  | |~~\\ |     )  ~------~`\\\n"
            " /' |  | |   /     ____ /~~~)\n"
            "(_/'   | | |     /'    |    ( |\n"
            "       | | |     \\    /   __)/ \\\n"
            "       \\  \\ \\      \\/    /' \\   `\\\n"
            "         \\  \\|\\        /   | |\\___|\n"
            "           \\ |  \\____/     | |\n"
            "           /^~>  \\        _/ <\n"
            "          |  |         \\       \\\n"
            "          |  | \\        \\        \\\n"
            "          -^-\\  \\       |        )\n"
            "               `\\_______/^\\______/\n"
        ),
        # Option 3: long dog
        (
            "                                  .-.\n"
            "     (___________________________()6 `-, \n"
            "     (   ______________________   /''\"`\n"
            "     //\\                      //\\\n"
            "    ""  ""                     "" "" \n"
        ),
        # Option 4: pufferfish
        (
            "                          . \n"
            "                          A       ;\n"
            "                |   ,--,-/ \\---,-/|  , \n"
            "               _|\,'. /|      /|   `/|-. \n"
            "           \`.'    /|      ,            `;. \n"
            "          ,'\   A     A         A   A _ /| `.; \n"
            "        ,/  _              A       _  / _   /|  ; \n"
            "       /\  / \\   ,  ,           A  /    /     `/| \n"
            "      /_| | _ \\         ,     ,             ,/  \\ \n"
            "     // | |/ `.\  ,-      ,       ,   ,/ ,/      \\/ \n"
            "     / @| |@  / /'   \\  \\      ,              >  /|    ,--. \n"
            "    |\_/   \_/ /      |  |           ,  ,/        \\  ./' __:.. \n"
            "    |  __ __  |       |  | .--.  ,         >  >   |-'   /     ` \n"
            "  ,/| /  '  \\ |       |  |     \\      ,           |    / \n"
            " /  |<--.__,->|       |  | .    `.        >  >    /   ( \n"
            "/_,' \\\\  ^  /  \\     /  /   `.    >--            /^\   | \n"
            "      \\\\___/    \\   /  /      \\__'     \\   \\   \\/   \\  | \n"
            "       `.   |/          ,  ,                  /`\\    \\  ) \n"
            "         \\  '  |/    ,       V    \\          /        `-\ \n"
            "          `|/  '  V      V           \\    \\.'            \\_ \n"
            "           '`-.       V       V        \\./'\\ \n"
            "               `|/-.      \\ /   \ /,---`\\          \n"
            "                /   `._____V_____V' \n"
        ),
        # Option 5: bart
        (
            "  |\\/\\/\\/|  \n"
            "  |      |  \n"
            "  |      |  \n"
            "  | (o)(o)  \n"
            "  C      _) \n"
            "   | ,___|  \n"
            "   |   /    \n"
            "  /____\\    \n"
            " /      \\   \n"
        ),
        # Option 6: Lara Croft

        (
            "       ,==;,       \n"
            "       )a,a\\g      \n"
            "       \\=_/8       \n"
            "       _| (_3,     \n"
            "      /(__/\\ ]\\    \n"
            "     (_,,__) \\\\    \n"
            "     //\\  ;/  \\\\   \n"
            "    //  )__\\   \\|_ \n"
            "  _'/  |[]__L,  ,>}\n"
            " /t}  / ,   [|     \n"
            "6    /-.|=._|/     \n"
            "    /  .'`-/`      \n"
            "   ( .' | /        \n"
            "   \\ |  ( |        \n"
            "    \\_)  \\_).      \n"
            "     \\ \\  \\ |      \n"
            "      \\ >  >|      \n"
            " snd /.'  / /      \n"
            "         '-'       \n"
        )
    ]

    def add_to_watchList(self, film):
        self.watchList.append(film)

    def remove_from_watchlist(self, film):
        self.watchList.remove(film)

    def pop_from_watchlist(self, film_index):
        return self.watchList.pop(film_index)

    def remove_from_watchlist_by_name(self, film_name):
        return self.remove_from_watchlist_by_property(
            lambda film: self.name, film_name
        )

    def remove_from_watchlist_by_actors(self, actor_list):
        removal_list = []

        for film in self.watchList:
            can_exit = False
            #if property_getter(film) == property_value:
            #    removal_list.push(film)
            for actor in actor_list:
                for film_actor in film.cast:
                    if actor == film_actor.name:
                        removal_list.push(film)
                        can_exit = True
                        break

                if can_exit: break
                

        for film in removal_list:
            self.watchList.remove(film)

        return len(removal_list)

    def get_watch_list(self):
        return self.watchList
    
    def get_films_added(self):
        return self.films_added

    def set_films_added(self, value):
        self.films_added = value

    def display_watchlist(self, displaying_other_user = False):
        if not displaying_other_user:
            if not self.watchList:
                print("\nYour watchlist is currently empty")
                return
            print("\nYour Watchlist:")
        for i, film in enumerate(self.watchList):
            print(f"{i+1}: {film.name}")
            print(f"  Description: {film.description}")
            print("  Actors:")
            for actor in film.cast:
                print(f"{actor.name} as {actor.role}")
            print("Comments:")
            for comment in film.comments:
                comment.display_comment()
            
    def add_rating(self, film_name, rating):
        if rating < 0 or rating > 10:
            raise IndexError("Rating value not in range 0-10")
            return

        self.ratings.update({film_name: rating})

    def get_rating(self, film_name):
        if not film_name in self.ratings:
            return None
        return self.ratings[film_name]
        
    def get_watch_list(self):
        return self.watchList
    
    def set_default_avatar(self):
        avatar=(
            "   /\\ \n"
            "  /  \\ \n"
            " |o  o|\n"
            "  \\ - /\n"
            "   \\_/\n"
        )
        return avatar

    def display_profile(self):
        print("\n--- Profile: " + self.username + " ---")
        print(self.avatar_ascii)
        print(f"Username: {self.username}")
        print(f"Favourite Film: {self.favFilm}")
        print(f"Films in Watchlist: {len(self.watchList)}")
        print("---------------------------\n")

    def get_dislikes(self):
        return self.dislikes

    def dislike_film(self, film):
        if film not in self.dislikes:
            self.dislikes.append(film)
            return film
        return None

    def undislike_film(self, film):
        self.dislikes.remove(film)

    def add_comment(self,film, comment):
        self.comments.update({film,comment})

    def change_avatar(self,index:int)->bool:
        # Sets avatar to what the user has selected
        if 0<=index < len(self.AVATAR_OPTIONS):
            self.avatar_index=index
            self.avatar_ascii = User.AVATAR_OPTIONS[index]
            return True
        return False
    
    def change_favFilm(self, film_name:str):
        self.favFilm=film_name
        print(f"Favourite Film Updated to: {self.favFilm}")
