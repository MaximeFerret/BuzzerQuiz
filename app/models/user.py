class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password  # Note: à sécuriser avec un hash

    def __repr__(self):
        return f"User({self.username}, {self.email})"
