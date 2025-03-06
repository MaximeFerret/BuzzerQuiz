from backend.business_object.quiz import Quiz, Question
from backend.business_object.db import db


class QuizDAO:
    @staticmethod
    def get_quiz_by_code(code):
        """Récupérer un quiz par son code."""
        return Quiz.query.filter_by(code=code).first()

    @staticmethod
    def get_quiz_by_id(quiz_id):
        """Récupérer un quiz par son ID."""
        return Quiz.query.get(quiz_id)

    @staticmethod
    def get_quizzes_by_creator_id(creator_id):
        """Récupérer tous les quiz créés par un utilisateur."""
        return Quiz.query.filter_by(creator_id=creator_id).all()

    @staticmethod
    def add_quiz(title, code, creator_id):
        """Ajouter un quiz dans la base de données."""
        try:
            quiz = Quiz(title=title, code=code, creator_id=creator_id)
            db.session.add(quiz)
            db.session.commit()  # S'assurer que quiz.id est disponible avant d'ajouter des questions
            return quiz  # Retourne l'objet pour l'utiliser dans d'autres opérations
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Erreur lors de l'ajout du quiz: {str(e)}")

    @staticmethod
    def delete_quiz(quiz):
        """Supprimer un quiz."""
        try:
            db.session.delete(quiz)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Erreur lors de la suppression du quiz: {str(e)}")

    @staticmethod
    def get_questions_by_quiz_id(quiz_id):
        """Récupérer toutes les questions d'un quiz."""
        return Question.query.filter_by(quiz_id=quiz_id).all()

    @staticmethod
    def delete_questions_by_quiz_id(quiz_id):
        """Supprimer toutes les questions d'un quiz."""
        try:
            Question.query.filter_by(quiz_id=quiz_id).delete()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Erreur lors de la suppression des questions: {str(e)}")

    @staticmethod
    def add_question(question):
        """Ajouter une question à un quiz."""
        try:
            db.session.add(question)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Erreur lors de l'ajout d'une question: {str(e)}")

    @staticmethod
    def commit():
        """Committer la transaction."""
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Erreur lors du commit: {str(e)}")

    @staticmethod
    def rollback():
        """Annuler la transaction."""
        db.session.rollback()
