class User:
    AVATAR_OPTIONS=[
        #Got these from https://www.asciiart.eu
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

    def __init__(self, username,avatar_index=0):
        self.username = username
        self.watchList=[]
        self.films_added=0
        # A dictionary associating film names with their ratings (0-10)
        self.ratings = {}
        self.avatar_index = avatar_index

        #Set ASCII based on the index above from database
        if 0 <= self.avatar_index < len(User.AVATAR_OPTIONS):
             self.avatar_ascii = User.AVATAR_OPTIONS[self.avatar_index]
        else:
             self.avatar_ascii = User.AVATAR_OPTIONS[0] # Fallback

    def add_to_watchList(self, film):
        self.watchList.append(film)

    def get_watch_list(self):
        return self.watchList
    
    def get_films_added(self):
        return self.films_added

    def set_films_added(self, value):
        self.films_added = value

    def display_watchlist(self):
        if not self.watchList:
            print("\nYour watchlist is currently empty")
            return
        print("\nYour Watchlist:")
        for i, film in enumerate(self.watchList):
            print("Film Name: "f"{film.name}")
            print("Description: "f"{film.description}")
            print("Actors:")
            for actor in film.cast:
                print(f"{actor.name} as {actor.role}")
            
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
        print(f"Films in Watchlist: {len(self.watchList)}")
        print("---------------------------\n")

    def change_avatar(self,index:int)->bool:
        # Sets avatar to what the user has selected
        if 0<=index < len(self.AVATAR_OPTIONS):
            self.avatar_index=index
            self.avatar_ascii = User.AVATAR_OPTIONS[index]
            return True
        return False