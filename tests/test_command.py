import unittest

from app.models.command import (PressBuzzerCommand, StartQuizCommand,
                                ValidateAnswerCommand)
from app.models.session import QuizSession


class TestCommandPattern(unittest.TestCase):
    def setUp(self):
        self.session = QuizSession()
        self.session.__init__()  # Réinitialiser la session pour chaque test

    def test_start_quiz_command(self):
        command = StartQuizCommand(self.session)
        command.execute()
        self.assertTrue(self.session.quiz_started)

    def test_press_buzzer_command(self):
        player = "Alice"
        command = PressBuzzerCommand(self.session, player)
        command.execute()
        self.assertIn(player, self.session.buzzer_queue)

    def test_validate_answer_command_correct(self):
        player = "Alice"
        self.session.press_buzzer(player)
        command = ValidateAnswerCommand(self.session, player, True)
        next_player = command.execute()
        self.assertIsNone(next_player)
        self.assertEqual(self.session.results[-1], {player: "Correct"})

    def test_validate_answer_command_incorrect(self):
        player1 = "Alice"
        player2 = "Bob"
        self.session.press_buzzer(player1)
        self.session.press_buzzer(player2)
        command = ValidateAnswerCommand(self.session, player1, False)
        next_player = command.execute()
        self.assertEqual(next_player, player2)
        self.assertEqual(self.session.results[-1], {player1: "Incorrect"})


if __name__ == "__main__":
    unittest.main()
