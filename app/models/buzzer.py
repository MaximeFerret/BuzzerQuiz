class Buzzer:
    def __init__(self):
        self.buzzer_queue = []

    def press(self, player):
        if player not in self.buzzer_queue:
            self.buzzer_queue.append(player)

    def get_next(self):
        if self.buzzer_queue:
            return self.buzzer_queue.pop(0)  # Retourne le premier
        return None

    def reset(self):
        self.buzzer_queue = []
