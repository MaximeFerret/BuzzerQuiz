from flask import Blueprint, jsonify, request

from app.models.session import QuizSession

buzzer_routes = Blueprint("buzzer_routes", __name__)


@buzzer_routes.route("/buzzer", methods=["POST"])
def press_buzzer():
    data = request.json
    player = data.get("player")

    if not player:
        return jsonify({"error": "Player name required"}), 400

    session = QuizSession()
    session.press_buzzer(player)
    return jsonify({"message": f"{player} pressed the buzzer"}), 200


@buzzer_routes.route("/buzzer/next", methods=["GET"])
def get_next():
    session = QuizSession()
    next_player = session.get_next_player()

    if next_player:
        return jsonify({"next_player": next_player}), 200
    else:
        return jsonify({"message": "No players in queue"}), 200


@buzzer_routes.route("/buzzer/reset", methods=["POST"])
def reset_buzzer():
    session = QuizSession()
    session.reset_buzzer()
    return jsonify({"message": "Buzzer queue reset"}), 200
