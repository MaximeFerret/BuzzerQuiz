from app.utils.singleton import Singleton


class QuizSession(Singleton):
    def __init__(self):
        if not hasattr(self, "initialized"):
            self.initialized = True
            self.players = []
            self.current_question = None
            self.quiz_started = False

    def start_quiz(self):
        self.quiz_started = True

    def add_player(self, player):
        self.players.append(player)
