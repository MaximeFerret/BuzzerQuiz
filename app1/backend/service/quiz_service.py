from ..dao.quiz_dao import QuizDAO
from ..business_object.quiz import Quiz, Question
from ..utils.generateur_code import generate_quiz_code

class QuizService:
    @staticmethod
    def create_quiz(title, creator_id):
        code = generate_quiz_code()
        quiz = QuizDAO.add_quiz(title, code, creator_id)
        return quiz

    @staticmethod
    def get_quiz_by_code(code):
        return QuizDAO.get_quiz_by_code(code)

    @staticmethod
    def get_quiz_by_id(quiz_id):
        return QuizDAO.get_quiz_by_id(quiz_id)

    @staticmethod
    def get_quizzes_by_creator_id(creator_id):
        return QuizDAO.get_quizzes_by_creator_id(creator_id)

    @staticmethod
    def delete_quiz(quiz):
        QuizDAO.delete_questions_by_quiz_id(quiz.id)
        QuizDAO.delete_quiz(quiz)

    @staticmethod
    def add_question_to_quiz(quiz_id, question_text, has_choices, options,
                             correct_answer):
        question = Question(
            quiz_id=quiz_id,
            question_text=question_text,
            has_choices=has_choices,
            option1=options[0] if len(options) > 0 else None,
            option2=options[1] if len(options) > 1 else None,
            option3=options[2] if len(options) > 2 else None,
            option4=options[3] if len(options) > 3 else None,
            correct_answer=correct_answer
        )
        QuizDAO.add_question(question)

    @staticmethod
    def get_questions_by_quiz_id(quiz_id):
        return QuizDAO.get_questions_by_quiz_id(quiz_id)
    
    @staticmethod
    def delete_questions_by_quiz_id(quiz_id):
        QuizDAO.delete_questions_by_quiz_id(quiz_id)
