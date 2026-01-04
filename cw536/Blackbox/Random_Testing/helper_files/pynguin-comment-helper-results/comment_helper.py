"""
Comment helper class for Pynguin testing
Includes profanity filter without external dependencies
"""

import re


def load_profan():
    """
    Load profanity words (simplified version for testing)
    Returns a basic set of common profanity words
    """
    # Basic profanity list for testing
    return {
        "badword",
        "offensive",
        "inappropriate",
        "vulgar",
        "curse"
    }


def censor(text):
    """
    Censor profanity in text
    Replaces profane words with asterisks
    """
    if not text:
        return text

    profanity_words = load_profan()

    if not profanity_words:
        return text

    def replace(match):
        word = match.group()
        return "*" * len(word)

    # Create regex pattern for word boundaries
    pattern = r"\b(" + "|".join(map(re.escape, profanity_words)) + r")\b"
    return re.sub(pattern, replace, text, flags=re.IGNORECASE)


class Comment:
    """Comment class with profanity filtering"""

    def __init__(self, message, user="Anonymous"):
        """
        Initialize comment with message and user
        Message is automatically censored for profanity
        """
        self.user = user  # username not user object
        self.message = censor(message)

    def display_comment(self):
        """Display the comment"""
        print(self.user, "\n", self.message)
        return f"{self.user}\n{self.message}"

    def get_message(self):
        """Get the censored message"""
        return self.message

    def get_user(self):
        """Get the username"""
        return self.user

    def set_user(self, user):
        """Change the username"""
        self.user = user
        return True

    def has_profanity(self):
        """Check if the original message likely had profanity (has asterisks)"""
        return "*" in self.message

    def message_length(self):
        """Get the length of the message"""
        return len(self.message)

    def is_anonymous(self):
        """Check if the comment is anonymous"""
        return self.user == "Anonymous"


# Additional helper functions for testing
def create_comment(message, user="Anonymous"):
    """Factory function to create a comment"""
    return Comment(message, user)


def create_multiple_comments(messages, user="Anonymous"):
    """Create multiple comments from a list of messages"""
    return [Comment(msg, user) for msg in messages]


def display_all_comments(comments):
    """Display all comments in a list"""
    results = []
    for comment in comments:
        results.append(comment.display_comment())
    return results