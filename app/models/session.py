from app.utils.singleton import Singleton


class QuizSession(Singleton):
    def __init__(self):
        if not hasattr(self, "initialized"):  # Vérifier si l'init a déjà été exécuté
            self.initialized = True
            self.players = []
            self.current_question = None
            self.quiz_started = False
            self.results = []
            self.buzzer_queue = []  # Liste d'attente des joueurs ayant buzzé

    def start_quiz(self):
        self.quiz_started = True

    def add_player(self, player):
        if player not in self.players:
            self.players.append(player)

    def press_buzzer(self, player):
        if player not in self.buzzer_queue:
            self.buzzer_queue.append(player)

    def get_next_player(self):
        if self.buzzer_queue:
            return self.buzzer_queue.pop(0)  # Retire et retourne le premier de la liste
        return None

    def reset_buzzer(self):
        self.buzzer_queue = []

    def validate_answer(self, player, correct):
        if correct:
            self.results.append({player: "Correct"})
        else:
            self.results.append({player: "Incorrect"})
