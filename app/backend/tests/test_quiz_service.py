import sys
import os
import unittest
from unittest.mock import patch, MagicMock
from app.backend.service.quiz_service import QuizService
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '../../')))


class TestQuizService(unittest.TestCase):

    @patch('app.backend.dao.quiz_dao.QuizDAO.add_quiz')
    @patch('app.backend.service.quiz_service.generate_quiz_code')
    def test_create_quiz(self, mock_generate_code, mock_add_quiz):
        # GIVEN
        title = "Test Quiz"
        creator_id = 1
        mock_generate_code.return_value = 'ABC123'
        mock_add_quiz.return_value = {
            'id': 1,
            'title': title,
            'code': 'ABC123',
            'creator_id': creator_id
        }

        # WHEN
        result = QuizService.create_quiz(title, creator_id)

        # THEN
        mock_generate_code.assert_called_once()
        mock_add_quiz.assert_called_once_with(title, 'ABC123', creator_id)
        self.assertEqual(result['code'], 'ABC123')

    @patch('app.backend.dao.quiz_dao.QuizDAO.get_quiz_by_code')
    def test_get_quiz_by_code(self, mock_get_quiz_by_code):
        # GIVEN
        code = "ABC123"
        mock_get_quiz_by_code.return_value = {
            'id': 1,
            'title': "Test Quiz",
            'code': code
        }

        # WHEN
        result = QuizService.get_quiz_by_code(code)

        # THEN
        mock_get_quiz_by_code.assert_called_once_with(code)
        self.assertEqual(result['code'], code)

    @patch('app.backend.dao.quiz_dao.QuizDAO.get_quiz_by_id')
    def test_get_quiz_by_id(self, mock_get_quiz_by_id):
        # GIVEN
        quiz_id = 1
        mock_get_quiz_by_id.return_value = {
            'id': quiz_id,
            'title': "Test Quiz"
        }

        # WHEN
        result = QuizService.get_quiz_by_id(quiz_id)

        # THEN
        mock_get_quiz_by_id.assert_called_once_with(quiz_id)
        self.assertEqual(result['id'], quiz_id)

    @patch('app.backend.dao.quiz_dao.QuizDAO.add_question')
    def test_add_question_to_quiz(self, mock_add_question):
        # GIVEN
        quiz_id = 1
        question_text = "What is 2+2?"
        has_choices = True
        options = ["1", "2", "3", "4"]
        correct_answer = "4"

        # WHEN
        QuizService.add_question_to_quiz(quiz_id, question_text, has_choices,
                                         options, correct_answer)

        # THEN
        mock_add_question.assert_called_once()
        added_question = mock_add_question.call_args[0][0]
        self.assertEqual(added_question.quiz_id, quiz_id)
        self.assertEqual(added_question.correct_answer, correct_answer)

    @patch('app.backend.dao.quiz_dao.QuizDAO.delete_quiz')
    @patch('app.backend.dao.quiz_dao.QuizDAO.delete_questions_by_quiz_id')
    def test_delete_quiz(self, mock_delete_questions, mock_delete_quiz):
        # GIVEN
        quiz = MagicMock()
        quiz.id = 1

        # WHEN
        QuizService.delete_quiz(quiz)

        # THEN
        mock_delete_questions.assert_called_once_with(quiz.id)
        mock_delete_quiz.assert_called_once_with(quiz)


if __name__ == '__main__':
    unittest.main()
