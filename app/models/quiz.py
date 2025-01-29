class Quiz:
    def __init__(self, title, creator):
        self.title = title
        self.creator = creator
        self.questions = []

    def add_question(self, question):
        self.questions.append(question)
