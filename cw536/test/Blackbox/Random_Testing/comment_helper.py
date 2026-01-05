import re

def load_profan():
    return {
        "badword",
        "offensive",
        "inappropriate",
        "vulgar",
        "curse"
    }


def censor(text):
    if not text:
        return text

    profanity_words = load_profan()

    if not profanity_words:
        return text

    def replace(match):
        word = match.group()
        return "*" * len(word)

    pattern = r"\b(" + "|".join(map(re.escape, profanity_words)) + r")\b"
    return re.sub(pattern, replace, text, flags=re.IGNORECASE)


class Comment:
    def __init__(self, message, user="Anonymous"):
        self.user = user  # username not user object
        self.message = censor(message)

    def display_comment(self):
        print(self.user, "\n", self.message)
        return f"{self.user}\n{self.message}"

    def get_message(self):
        return self.message

    def get_user(self):
        return self.user

    def set_user(self, user):
        self.user = user
        return True

    def has_profanity(self):
        return "*" in self.message

    def message_length(self):
        return len(self.message)

    def is_anonymous(self):
        return self.user == "Anonymous"


def create_comment(message, user="Anonymous"):
    return Comment(message, user)


def create_multiple_comments(messages, user="Anonymous"):
    return [Comment(msg, user) for msg in messages]


def display_all_comments(comments):
    results = []
    for comment in comments:
        results.append(comment.display_comment())
    return results