class Buzzer:
    def __init__(self):
        self.buzzers = []

    def buzz(self, user):
        if user not in self.buzzers:
            self.buzzers.append(user)

    def get_first(self):
        return self.buzzers[0] if self.buzzers else None

    def next(self):
        if self.buzzers:
            return self.buzzers.pop(0)
        return None
