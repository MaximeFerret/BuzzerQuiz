from ..business_object.quiz import Quiz, Question
from ..business_object.db import db


class QuizDAOError(Exception):
    """Exception spécifique pour les erreurs de QuizDAO."""
    pass


class QuizDAO:
    @staticmethod
    def get_quiz_by_code(code):
        """Récupérer un quiz par son code.

        Cette méthode permet de récupérer un quiz par son code.

        Parameters:
        -----------
            code (str): le code du quiz.

        Returns:
        --------
            Quiz: le quiz récupéré.
        """
        return Quiz.query.filter_by(code=code).first()

    @staticmethod
    def get_quiz_by_id(quiz_id):
        """Récupérer un quiz par son ID.

        Cette méthode permet de récupérer un quiz par son ID.

        Parameters:
        -----------
            quiz_id (int): l'ID du quiz.

        Returns:
        --------
            Quiz: le quiz récupéré.
        """
        return Quiz.query.get(quiz_id)

    @staticmethod
    def get_quizzes_by_creator_id(creator_id):
        """Récupérer tous les quiz créés par un utilisateur.

        Cette méthode permet de récupérer tous les quiz créés par un
        utilisateur.

        Parameters:
        -----------
            creator_id (int): l'ID de l'utilisateur.

        Returns:
        --------
            list: les quiz récupérés.
        """
        return Quiz.query.filter_by(creator_id=creator_id).all()

    @staticmethod
    def add_quiz(title, code, creator_id):
        """Ajouter un quiz dans la base de données.

        Cette méthode permet d'ajouter un quiz dans la base de données.

        Parameters:
        -----------
            title (str): le titre du quiz.
            code (str): le code du quiz.
            creator_id (int): l'ID de l'utilisateur.

        Returns:
        --------
            Quiz: le quiz ajouté.
        """
        try:
            quiz = Quiz(title=title, code=code, creator_id=creator_id)
            db.session.add(quiz)
            db.session.commit()
            return quiz
        except Exception as e:
            db.session.rollback()
            raise QuizDAOError(
                f"Erreur lors de l'ajout du quiz: {str(e)}"
            ) from e

    @staticmethod
    def delete_quiz(quiz):
        """Supprimer un quiz.

        Cette méthode permet de supprimer un quiz.

        Parameters:
        -----------
            quiz (Quiz): le quiz à supprimer.

        Returns:
        --------
            None.
        """
        try:
            db.session.delete(quiz)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise QuizDAOError(
                f"Erreur lors de la suppression du quiz: {str(e)}"
            ) from e

    @staticmethod
    def get_questions_by_quiz_id(quiz_id):
        """Récupérer toutes les questions d'un quiz.

        Cette méthode permet de récupérer toutes les questions d'un quiz.

        Parameters:
        -----------
            quiz_id (int): l'ID du quiz.

        Returns:
        --------
            list: les questions récupérées.
        """
        return Question.query.filter_by(quiz_id=quiz_id).all()

    @staticmethod
    def delete_questions_by_quiz_id(quiz_id):
        """Supprimer toutes les questions d'un quiz.

        Cette méthode permet de supprimer toutes les questions d'un quiz.

        Parameters:
        -----------
            quiz_id (int): l'ID du quiz.

        Returns:
        --------
            None.
        """
        try:
            Question.query.filter_by(quiz_id=quiz_id).delete()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise QuizDAOError(
                f"Erreur lors de la suppression des questions: {str(e)}"
            ) from e

    @staticmethod
    def add_question(question):
        """Ajouter une question à un quiz.

        Cette méthode permet d'ajouter une question à un quiz.

        Parameters:
        -----------
            question (Question): la question à ajouter.

        Returns:
        --------
            Question: la question ajoutée.
        """
        try:
            db.session.add(question)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise QuizDAOError(
                f"Erreur lors de l'ajout d'une question: {str(e)}"
            ) from e

    @staticmethod
    def commit():
        """Committer la transaction.

        Cette méthode permet de committer la transaction.

        Returns:
        --------
            None.
        """
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise QuizDAOError(f"Erreur lors du commit: {str(e)}") from e

    @staticmethod
    def rollback():
        """Annuler la transaction.

        Cette méthode permet d'annuler la transaction.

        Returns:
        --------
            None.
        """
        db.session.rollback()
