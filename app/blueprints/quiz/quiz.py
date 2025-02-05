from datetime import datetime, timedelta, timezone

from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)
from flask_login import current_user, login_required
from models.db import db
from models.quiz import Question, Quiz

quiz_bp = Blueprint("quiz", __name__, template_folder="templates")


def check_session():
    if not session.get("is_user") or "user_last_active" not in session:
        flash("Veuillez vous connecter.", "warning")
        return redirect(url_for("authentication.login"))

    # Vérifie le temps d'inactivité
    last_active = session.get("user_last_active")
    if datetime.now(timezone.utc) - last_active > timedelta(minutes=10):
        session.pop("is_user", None)
        session.pop("user_last_active", None)
        flash("Session expirée. Veuillez vous reconnecter.", "warning")
        return redirect(url_for("authentication.login"))

    # Met à jour le dernier moment d'activité
    session["user_last_active"] = datetime.now(timezone.utc)
    return None  # Aucune redirection, l'utilisateur est actif


@quiz_bp.route("/start", methods=["GET"])
@login_required
def start_quiz():
    session_check = check_session()
    if session_check:
        return session_check  # Redirige si la session est expirée

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
    session_check = check_session()
    if session_check:
        return session_check

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
    session_check = check_session()
    if session_check:
        return session_check

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
    session_check = check_session()
    if session_check:
        return session_check

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
    session_check = check_session()
    if session_check:
        return session_check

    quiz = Quiz.query.get_or_404(quiz_id)

    # Si l'utilisateur n'est pas le créateur du quiz, tu peux le rediriger
    if quiz.creator_id != current_user.id:
        return redirect(url_for("quiz.start_quiz"))

    return render_template("start_quiz_game.html", quiz=quiz)
