from flask import Blueprint, jsonify, redirect, request, url_for

from app.models.command import (PressBuzzerCommand, StartQuizCommand,
                                ValidateAnswerCommand)
from app.models.session import QuizSession

command_routes = Blueprint("command_routes", __name__)


@command_routes.route("/start_quiz", methods=["POST"])
def start_quiz():
    session = QuizSession()
    command = StartQuizCommand(session)
    command.execute()
    return jsonify({"message": "Quiz started"}), 200


@command_routes.route("/press_buzzer", methods=["POST"])
def press_buzzer():
    data = request.json
    player = data.get("player")

    if not player:
        return jsonify({"error": "Player name required"}), 400

    session = QuizSession()
    command = PressBuzzerCommand(session, player)
    command.execute()
    return jsonify({"message": f"{player} pressed the buzzer"}), 200


@command_routes.route("/validate_answer", methods=["POST"])
def validate_answer():
    data = request.json
    player = data.get("player")
    correct = data.get("correct")

    if player is None or correct is None:
        return jsonify({"error": "Player and correct status required"}), 400

    session = QuizSession()
    command = ValidateAnswerCommand(session, player, correct)
    next_player = command.execute()

    if next_player:
        return (
            jsonify(
                {"message": f"{player}'s answer was incorrect, next: {next_player}"}
            ),
            200,
        )
    else:
        return jsonify({"message": f"{player}'s answer was correct"}), 200
