class Command:
    def execute(self):
        pass


class StartQuizCommand(Command):
    def __init__(self, session):
        self.session = session

    def execute(self):
        self.session.start_quiz()


class ValidateAnswerCommand(Command):
    def __init__(self, session, answer):
        self.session = session
        self.answer = answer

    def execute(self):
        # Logique de validation de réponse
        pass
