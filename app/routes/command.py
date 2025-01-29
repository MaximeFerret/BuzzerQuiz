from flask import Blueprint

from app.models.command import StartQuizCommand
from app.models.session import QuizSession

command = Blueprint("command", __name__)


@command.route("/start_quiz", methods=["POST"])
def start_quiz():
    session = QuizSession()
    command = StartQuizCommand(session)
    command.execute()
    return "Quiz Started"
