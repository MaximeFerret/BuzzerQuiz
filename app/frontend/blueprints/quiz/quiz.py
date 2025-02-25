from datetime import datetime, timedelta, timezone

from backend.models.db import db
from backend.models.quiz import Answer, Question, Quiz
from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)
from flask_login import current_user, login_required

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

        question_count = int(request.form.get("question_count", 0))

        for i in range(question_count):
            question_text = request.form.get(f"question_{i}")
            if question_text:
                new_question = Question(text=question_text, quiz_id=new_quiz.id)
                db.session.add(new_question)
                db.session.commit()

                # Ajouter les choix associés à la question
                for j in range(4):  # Maximum de 4 choix
                    choice_text = request.form.get(f"question_{i}_choice_{j}")
                    if choice_text:
                        new_choice = Answer(
                            text=choice_text, question_id=new_question.id
                        )
                        db.session.add(new_choice)
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
        quiz_title = request.form["title"]
        quiz.title = quiz_title  # Modifie le titre du quiz
        db.session.commit()

        # Gérer les questions et les choix
        question_count = int(request.form.get("question_count", 0))

        # Suppression des anciennes questions et choix (si nécessaire)
        for question in quiz.questions:
            db.session.delete(question)
        db.session.commit()

        # Ajouter les nouvelles questions
        for i in range(question_count):
            question_text = request.form.get(f"question_{i}")
            if question_text:
                new_question = Question(text=question_text, quiz_id=quiz.id)
                db.session.add(new_question)
                db.session.commit()

                # Ajouter les choix associés à la question
                for j in range(4):  # Maximum de 4 choix
                    choice_text = request.form.get(f"question_{i}_choice_{j}")
                    if choice_text:
                        new_choice = Answer(
                            text=choice_text, question_id=new_question.id
                        )
                        db.session.add(new_choice)
                        db.session.commit()

        db.session.commit()

    # Récupérer les questions et les choix du quiz
    questions = quiz.questions
    return render_template("edit_quiz_form.html", quiz=quiz, questions=questions)


@quiz_bp.route("/quiz/<int:quiz_id>/update", methods=["POST"])
def update_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)

    # Mettre à jour le titre
    quiz.title = request.form.get("title")

    # Supprimer les questions marquées
    for q_id in request.form.getlist("remove_question[]"):
        Question.query.filter_by(id=q_id).delete()

    # Supprimer les choix marqués
    for c_id in request.form.getlist("remove_choice[]"):
        Answer.query.filter_by(id=c_id).delete()

    # Mettre à jour les questions existantes
    for question in quiz.questions:
        new_text = request.form.get(f"question_{question.id}")
        if new_text:  # Vérifie que le texte n'est pas vide
            question.text = new_text

        for choice in question.answers:
            choice_text = request.form.get(f"choice_{question.id}_{choice.id}")
            if choice_text:
                choice.text = choice_text  # Mise à jour du texte du choix

    # Ajouter les nouvelles questions
    for key, value in request.form.items():
        if "choice" in key and value.strip():  # On vérifie que la clé contient "choice"
            parts = key.split(
                "_"
            )  # Exemple: "question_2_choice_1" -> ["question", "2", "choice", "1"]

            if len(parts) == 4:  # Vérifie que la clé correspond bien à un choix
                question_id = int(parts[1])  # ID de la question associée

                # Vérifier si la question existe bien
                question = Question.query.get(question_id)
                if question:
                    new_choice = Answer(text=value, question_id=question.id)
                    db.session.add(new_choice)

        db.session.commit()
    return redirect(url_for("authentication.dashboard"))


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
