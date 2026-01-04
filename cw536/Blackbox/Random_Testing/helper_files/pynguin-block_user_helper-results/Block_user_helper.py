"""
Block/Unblock User helper for Pynguin testing
Simplified without file I/O and input() calls
"""


class UserDatabase:
    """Simple in-memory user database for testing"""

    def __init__(self):
        self.by_id = {}
        self.by_username = {}

    def add_user(self, user_id, username, friends=None, blocked=None):
        """Add a user to the database"""
        user = {
            "id": user_id,
            "username": username,
            "friends": friends if friends else [],
            "blocked": blocked if blocked else []
        }
        self.by_id[user_id] = user
        self.by_username[username] = user_id
        return user

    def get_user_by_id(self, user_id):
        """Get user record by ID"""
        return self.by_id.get(user_id)

    def get_user_id_by_username(self, username):
        """Get user ID by username"""
        return self.by_username.get(username)

    def user_exists(self, user_id):
        """Check if user exists"""
        return user_id in self.by_id


def block_user_safe(current_user_id, target_username, users_db):
    """
    Block a user (no input, returns status)

    Returns:
        - "success": User blocked successfully
        - "not_found": Target user not found
        - "self_block": Cannot block yourself
        - "already_blocked": User already blocked
        - "user_not_found": Current user not found
    """
    current_user = users_db.get_user_by_id(current_user_id)

    if not current_user:
        return "user_not_found"

    target_id = users_db.get_user_id_by_username(target_username)

    if not target_id:
        return "not_found"

    if target_id == current_user_id:
        return "self_block"

    if target_id in current_user["blocked"]:
        return "already_blocked"

    # Remove from friends if they are friends
    if target_id in current_user["friends"]:
        current_user["friends"].remove(target_id)

        target_user = users_db.get_user_by_id(target_id)
        if target_user and current_user_id in target_user["friends"]:
            target_user["friends"].remove(current_user_id)

    # Add to blocked list
    current_user["blocked"].append(target_id)

    return "success"


def unblock_user_safe(current_user_id, target_username, users_db):
    """
    Unblock a user (no input, returns status)

    Returns:
        - "success": User unblocked successfully
        - "not_blocked": User is not in blocked list
        - "not_found": Target user not found
        - "no_blocked_users": No users are blocked
        - "user_not_found": Current user not found
    """
    current_user = users_db.get_user_by_id(current_user_id)

    if not current_user:
        return "user_not_found"

    if not current_user["blocked"]:
        return "no_blocked_users"

    target_id = users_db.get_user_id_by_username(target_username)

    if not target_id:
        return "not_found"

    if target_id not in current_user["blocked"]:
        return "not_blocked"

    # Remove from blocked list
    current_user["blocked"].remove(target_id)

    return "success"


def is_user_blocked(current_user_id, target_user_id, users_db):
    """Check if a user is blocked"""
    current_user = users_db.get_user_by_id(current_user_id)
    if not current_user:
        return False
    return target_user_id in current_user.get("blocked", [])


def get_blocked_users(current_user_id, users_db):
    """Get list of blocked user IDs"""
    current_user = users_db.get_user_by_id(current_user_id)
    if not current_user:
        return []
    return current_user.get("blocked", [])


def get_blocked_usernames(current_user_id, users_db):
    """Get list of blocked usernames"""
    current_user = users_db.get_user_by_id(current_user_id)
    if not current_user:
        return []

    blocked_ids = current_user.get("blocked", [])
    usernames = []

    for user_id in blocked_ids:
        user = users_db.get_user_by_id(user_id)
        if user:
            usernames.append(user["username"])

    return usernames


def count_blocked_users(current_user_id, users_db):
    """Count how many users are blocked"""
    blocked = get_blocked_users(current_user_id, users_db)
    return len(blocked)


def can_interact(user1_id, user2_id, users_db):
    """Check if two users can interact (neither has blocked the other)"""
    user1 = users_db.get_user_by_id(user1_id)
    user2 = users_db.get_user_by_id(user2_id)

    if not user1 or not user2:
        return False

    # Check if either user has blocked the other
    if user2_id in user1.get("blocked", []):
        return False
    if user1_id in user2.get("blocked", []):
        return False

    return True


def block_and_unfriend(current_user_id, target_username, users_db):
    """
    Block a user and remove them from friends in one operation
    Returns tuple: (block_status, was_friend)
    """
    current_user = users_db.get_user_by_id(current_user_id)
    target_id = users_db.get_user_id_by_username(target_username)

    if not current_user or not target_id:
        return ("failed", False)

    was_friend = target_id in current_user.get("friends", [])
    status = block_user_safe(current_user_id, target_username, users_db)

    return (status, was_friend)


# Helper functions for testing
def create_sample_users():
    """Create sample user database for testing"""
    db = UserDatabase()

    db.add_user(1, "alice", friends=[2], blocked=[])
    db.add_user(2, "bob", friends=[1], blocked=[])
    db.add_user(3, "charlie", friends=[], blocked=[])

    return db


def setup_blocking_scenario():
    """Set up a scenario where alice blocks bob"""
    db = create_sample_users()
    block_user_safe(1, "bob", db)
    return db


def setup_complex_scenario():
    """Set up a complex scenario with multiple blocks"""
    db = UserDatabase()

    db.add_user(1, "alice", friends=[2, 3], blocked=[])
    db.add_user(2, "bob", friends=[1], blocked=[])
    db.add_user(3, "charlie", friends=[1], blocked=[])
    db.add_user(4, "dave", friends=[], blocked=[1])

    return db