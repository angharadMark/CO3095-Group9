class UserMessage:
    def __init__(self, sender_username, message, read = False):
        self.sender = sender_username
        self.message = message
        self.read = read

    @staticmethod
    def from_dict(message_dict):
        return UserMessage(message_dict["sender"],
            message_dict["message"],
            message_dict["read"]
        )

    def get_message(self):
        return self.message

    def get_sender_username(self):
        return self.sender

    def get_read_status(self):
        return self.read

    def mark_as_read(self):
        self.read = True

    def to_dict(self):
        return {
            "sender": self.sender,
            "message": self.message,
            "read": self.read
        }
