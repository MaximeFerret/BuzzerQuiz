from backend.models.quiz import Quiz, Question, Answer
from backend.models.db import db

class QuizDAO:
    @staticmethod
    def get_quiz_by_id(quiz_id):
        return Quiz.query.get(quiz_id)

    @staticmethod
    def get_quizzes_by_creator_id(creator_id):
        return Quiz.query.filter_by(creator_id=creator_id).all()

    @staticmethod
    def add_quiz(quiz):
        db.session.add(quiz)
        db.session.commit()

    @staticmethod
    def delete_quiz(quiz):
        db.session.delete(quiz)
        db.session.commit()

    @staticmethod
    def add_question(question):
        db.session.add(question)
        db.session.commit()

    @staticmethod
    def delete_question(question):
        db.session.delete(question)
        db.session.commit()

    @staticmethod
    def add_answer(answer):
        db.session.add(answer)
        db.session.commit()
