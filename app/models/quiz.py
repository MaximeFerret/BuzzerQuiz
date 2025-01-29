import uuid


class Question:
    def __init__(self, text):
        self.id = str(uuid.uuid4())
        self.text = text


class Quiz:
    def __init__(self, title, creator):
        self.id = str(uuid.uuid4())
        self.title = title
        self.creator = creator  # Lien avec User
        self.questions = []

    def add_question(self, question_text):
        question = Question(question_text)
        self.questions.append(question)

    def get_questions(self):
        return [q.text for q in self.questions]
