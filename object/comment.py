
class Comment:
    def __init__(self,message,user="Anonymous"):
        self.user = user
        self.message = message

    def display_comment(self):
        print(self.user, "\n", self.message)

    def edit_message(self, message):
        self.message = message
