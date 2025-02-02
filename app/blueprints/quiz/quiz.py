from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from models.db import db
from models.quiz import Question, Quiz

quiz_bp = Blueprint("quiz", __name__, template_folder="templates")


@quiz_bp.route("/start", methods=["GET"])
@login_required
def start_quiz():
    # Récupère tous les quiz créés par l'utilisateur connecté
    user_quizzes = Quiz.query.filter_by(creator_id=current_user.id).all()

    # Si l'utilisateur n'a pas créé de quiz, afficher un message
    if not user_quizzes:
        message = "Vous n'avez aucun quiz pour le moment."
    else:
        message = None

    return render_template("start_quiz.html", quizzes=user_quizzes, message=message)


@quiz_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_quiz():
    if request.method == "POST":
        quiz_title = request.form["title"]
        new_quiz = Quiz(title=quiz_title, creator_id=current_user.id)
        db.session.add(new_quiz)
        db.session.commit()
        return redirect(url_for("authentication.dashboard"))

    return render_template("create_quiz.html")


@quiz_bp.route("/edit", methods=["GET"])
@login_required
def edit_quiz():
    # Récupère tous les quiz créés par l'utilisateur connecté
    user_quizzes = Quiz.query.filter_by(creator_id=current_user.id).all()

    # Si l'utilisateur n'a pas créé de quiz, afficher un message
    if not user_quizzes:
        message = "Vous n'avez aucun quiz pour le moment."
    else:
        message = None

    return render_template("edit_quiz.html", quizzes=user_quizzes, message=message)


@quiz_bp.route("/edit/<int:quiz_id>", methods=["GET", "POST"])
@login_required
def edit_quiz_by_id(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)

    if quiz.creator_id != current_user.id:
        # Si l'utilisateur n'est pas le créateur du quiz, redirige-le
        return redirect(url_for("quiz.edit_quiz"))

    if request.method == "POST":
        question_text = request.form["question"]
        new_question = Question(text=question_text, quiz_id=quiz.id)
        db.session.add(new_question)
        db.session.commit()

    return render_template("edit_quiz.html", quiz=quiz)


@quiz_bp.route("/start/<int:quiz_id>", methods=["GET"])
@login_required
def start_quiz_by_id(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)

    # Si l'utilisateur n'est pas le créateur du quiz, tu peux le rediriger
    if quiz.creator_id != current_user.id:
        return redirect(url_for("quiz.start_quiz"))

    return render_template("start_quiz_game.html", quiz=quiz)
