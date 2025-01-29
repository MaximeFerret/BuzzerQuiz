from flask import Blueprint

quiz = Blueprint("quiz", __name__)


@quiz.route("/create_quiz")
def create_quiz():
    return "Create Quiz Page"
