from ..business_object.quiz import Question
from ..dao.quiz_dao import QuizDAO
from ..utils.generateur_code import generate_quiz_code


class QuizService:
    """
    Service pour les opérations liées aux quizzes.
    """

    @staticmethod
    def create_quiz(title, creator_id):
        """Créer un quiz

        Cette méthode permet de créer un quiz et de l'ajouter à la base de
        données.

        Parameters:
        -----------
            title (str): le titre du quiz.
            creator_id (int): l'identifiant de l'utilisateur qui crée le quiz.

        Return:
        -------
            Quiz: le quiz créé.
        """
        code = generate_quiz_code()
        return QuizDAO.add_quiz(title, code, creator_id)

    @staticmethod
    def get_quiz_by_code(code):
        """Obtenir un quiz par code

        Cette méthode permet d'obtenir un quiz par son code.

        Parameters:
        -----------
            code (str): le code du quiz.

        Return:
        -------
            Quiz: le quiz obtenu.
        """
        return QuizDAO.get_quiz_by_code(code)

    @staticmethod
    def get_quiz_by_id(quiz_id):
        """Obtenir un quiz par identifiant

        Cette méthode permet d'obtenir un quiz par son identifiant.

        Parameters:
        -----------
            quiz_id (int): l'identifiant du quiz.

        Return:
        -------
            Quiz: le quiz obtenu.
        """
        return QuizDAO.get_quiz_by_id(quiz_id)

    @staticmethod
    def get_quizzes_by_creator_id(creator_id):
        """Obtenir les quizzes par identifiant de créateur

        Cette méthode permet d'obtenir les quizzes par identifiant de créateur.

        Parameters:
        -----------
            creator_id (int): l'identifiant du créateur.

        Return:
        -------
            list: les quizzes obtenus.
        """
        return QuizDAO.get_quizzes_by_creator_id(creator_id)

    @staticmethod
    def delete_quiz(quiz):
        """Supprimer un quiz

        Cette méthode permet de supprimer un quiz et ses questions.

        Parameters:
        -----------
            quiz (Quiz): le quiz à supprimer.
        """
        QuizDAO.delete_questions_by_quiz_id(quiz.id)
        QuizDAO.delete_quiz(quiz)

    @staticmethod
    def add_question_to_quiz(
        quiz_id, question_text, has_choices, options, correct_answer
    ):
        """Ajouter une question à un quiz

        Cette méthode permet d'ajouter une question à un quiz.

        Parameters:
        -----------
            quiz_id (int): l'identifiant du quiz.
            question_text (str): le texte de la question.
            has_choices (bool): si la question a des options.
            options (list): les options de la question.
            correct_answer (int): la réponse correcte.
        """
        question = Question(
            quiz_id=quiz_id,
            question_text=question_text,
            has_choices=has_choices,
            option1=options[0] if len(options) > 0 else None,
            option2=options[1] if len(options) > 1 else None,
            option3=options[2] if len(options) > 2 else None,
            option4=options[3] if len(options) > 3 else None,
            correct_answer=correct_answer,
        )
        QuizDAO.add_question(question)

    @staticmethod
    def get_questions_by_quiz_id(quiz_id):
        """Obtenir les questions par identifiant de quiz

        Cette méthode permet d'obtenir les questions par identifiant de quiz.

        Parameters:
        -----------
            quiz_id (int): l'identifiant du quiz.

        Return:
        -------
            list: les questions obtenues.
        """
        return QuizDAO.get_questions_by_quiz_id(quiz_id)

    @staticmethod
    def delete_questions_by_quiz_id(quiz_id):
        QuizDAO.delete_questions_by_quiz_id(quiz_id)
