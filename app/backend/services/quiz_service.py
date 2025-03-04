from backend.dao.quiz_dao import QuizDAO
from backend.models.quiz import Quiz, Question, Answer

class QuizService:
    @staticmethod
    def create_quiz(title, creator_id, questions_data):
        new_quiz = Quiz(title=title, creator_id=creator_id)
        QuizDAO.add_quiz(new_quiz)

        for question_data in questions_data:
            question_text = question_data['text']
            new_question = Question(text=question_text, quiz_id=new_quiz.id)
            QuizDAO.add_question(new_question)

            for choice_text in question_data['choices']:
                new_choice = Answer(text=choice_text, question_id=new_question.id)
                QuizDAO.add_answer(new_choice)

    @staticmethod
    def get_quizzes_by_creator_id(creator_id):
        return QuizDAO.get_quizzes_by_creator_id(creator_id)

    @staticmethod
    def get_quiz_by_id(quiz_id):
        return QuizDAO.get_quiz_by_id(quiz_id)

    @staticmethod
    def delete_quiz(quiz_id):
        quiz = QuizDAO.get_quiz_by_id(quiz_id)
        if quiz:
            QuizDAO.delete_quiz(quiz)
