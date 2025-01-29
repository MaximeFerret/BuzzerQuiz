from abc import ABC, abstractmethod

from app.models.session import QuizSession


class Command(ABC):
    """Classe abstraite pour les commandes"""

    @abstractmethod
    def execute(self):
        pass


class StartQuizCommand(Command):
    """Commande pour démarrer un quiz"""

    def __init__(self, session):
        self.session = session

    def execute(self):
        self.session.start_quiz()


class PressBuzzerCommand(Command):
    """Commande pour gérer le buzzer d'un joueur"""

    def __init__(self, session, player):
        self.session = session
        self.player = player

    def execute(self):
        self.session.press_buzzer(self.player)


class ValidateAnswerCommand(Command):
    """Commande pour valider ou invalider une réponse"""

    def __init__(self, session, player, correct):
        self.session = session
        self.player = player
        self.correct = correct

    def execute(self):
        self.session.validate_answer(self.player, self.correct)
        if not self.correct:
            return (
                self.session.get_next_player()
            )  # Retourne le prochain joueur en attente
        return None
