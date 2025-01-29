from flask import Blueprint, jsonify, request

from app.models.quiz import Quiz
from app.models.session import QuizSession

quiz_routes = Blueprint("quiz_routes", __name__)

# Stockage temporaire des quiz
quizzes = {}


@quiz_routes.route("/create", methods=["POST"])
def create_quiz():
    data = request.json
    title = data.get("title")
    creator = data.get("creator")

    if not title or not creator:
        return jsonify({"error": "Title and creator required"}), 400

    quiz = Quiz(title, creator)
    quizzes[quiz.id] = quiz
    return jsonify({"message": "Quiz created", "quiz_id": quiz.id}), 201


@quiz_routes.route("/add_question", methods=["POST"])
def add_question():
    data = request.json
    quiz_id = data.get("quiz_id")
    question_text = data.get("question")

    quiz = quizzes.get(quiz_id)
    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404

    quiz.add_question(question_text)
    return jsonify({"message": "Question added"}), 200


@quiz_routes.route("/start/<quiz_id>", methods=["POST"])
def start_quiz(quiz_id):
    quiz = quizzes.get(quiz_id)
    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404

    session = QuizSession()
    session.start_quiz()
    return jsonify({"message": f"Quiz '{quiz.title}' started"}), 200
