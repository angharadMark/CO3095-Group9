from logic.profanity_filter import censor

class Comment:
    def __init__(self,message,user="Anonymous"):
        self.user = user #username not user object
        self.message = censor(message)

    def display_comment(self):
        print(self.user, "\n", self.message)

    def edit_message(self, message):
        self.message = censor(message)
    

