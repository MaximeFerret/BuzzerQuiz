from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required
from datetime import datetime, timedelta, timezone
from backend.services.quiz_service import QuizService
from backend.models.db import db
from backend.models.quiz import Answer, Question, Quiz

quiz_bp = Blueprint("quiz", __name__, template_folder="../../frontend/blueprints/quiz/templates")

def check_session():
    if not session.get("is_user") or "user_last_active" not in session:
        flash("Veuillez vous connecter.", "warning")
        return redirect(url_for("authentication.login"))

    last_active = session.get("user_last_active")
    if datetime.now(timezone.utc) - last_active > timedelta(minutes=10):
        session.pop("is_user", None)
        session.pop("user_last_active", None)
        flash("Session expirée. Veuillez vous reconnecter.", "warning")
        return redirect(url_for("authentication.login"))

    session["user_last_active"] = datetime.now(timezone.utc)
    return None

@quiz_bp.route("/start", methods=["GET"])
@login_required
def start_quiz():
    session_check = check_session()
    if session_check:
        return session_check

    user_quizzes = QuizService.get_quizzes_by_creator_id(current_user.id)
    message = "Vous n'avez aucun quiz pour le moment." if not user_quizzes else None

    return render_template("start_quiz.html", quizzes=user_quizzes, message=message)

@quiz_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_quiz():
    session_check = check_session()
    if session_check:
        return session_check

    if request.method == "POST":
        quiz_title = request.form["title"]
        question_count = int(request.form.get("question_count", 0))
        questions_data = []

        for i in range(question_count):
            question_text = request.form.get(f"question_{i}")
            choices = [request.form.get(f"question_{i}_choice_{j}") for j in range(4) if request.form.get(f"question_{i}_choice_{j}")]
            questions_data.append({"text": question_text, "choices": choices})

        QuizService.create_quiz(quiz_title, current_user.id, questions_data)
        return redirect(url_for("authentication.dashboard"))

    return render_template("create_quiz.html")

@quiz_bp.route("/edit", methods=["GET"])
@login_required
def edit_quiz():
    session_check = check_session()
    if session_check:
        return session_check

    user_quizzes = QuizService.get_quizzes_by_creator_id(current_user.id)
    message = "Vous n'avez aucun quiz pour le moment." if not user_quizzes else None

    return render_template("edit_quiz.html", quizzes=user_quizzes, message=message)

@quiz_bp.route("/edit/<int:quiz_id>", methods=["GET", "POST"])
@login_required
def edit_quiz_by_id(quiz_id):
    session_check = check_session()
    if session_check:
        return session_check

    quiz = QuizService.get_quiz_by_id(quiz_id)
    if quiz.creator_id != current_user.id:
        return redirect(url_for("quiz.edit_quiz"))

    if request.method == "POST":
        quiz_title = request.form["title"]
        quiz.title = quiz_title
        db.session.commit()

        question_count = int(request.form.get("question_count", 0))
        for question in quiz.questions:
            db.session.delete(question)
        db.session.commit()

        for i in range(question_count):
            question_text = request.form.get(f"question_{i}")
            if question_text:
                new_question = Question(text=question_text, quiz_id=quiz.id)
                db.session.add(new_question)
                db.session.commit()

                for j in range(4):
                    choice_text = request.form.get(f"question_{i}_choice_{j}")
                    if choice_text:
                        new_choice = Answer(text=choice_text, question_id=new_question.id)
                        db.session.add(new_choice)
                        db.session.commit()

        db.session.commit()

    questions = quiz.questions
    return render_template("edit_quiz_form.html", quiz=quiz, questions=questions)

@quiz_bp.route("/delete/<int:quiz_id>", methods=["GET"])
@login_required
def delete_quiz(quiz_id):
    session_check = check_session()
    if session_check:
        return session_check

    quiz = QuizService.get_quiz_by_id(quiz_id)
    if quiz.creator_id != current_user.id:
        flash("Vous n'êtes pas autorisé à supprimer ce quiz.", "danger")
        return redirect(url_for("quiz.edit_quiz"))

    QuizService.delete_quiz(quiz_id)
    flash("Quiz supprimé avec succès.", "success")
    return redirect(url_for("authentication.dashboard"))

@quiz_bp.route("/start/<int:quiz_id>", methods=["GET"])
@login_required
def start_quiz_by_id(quiz_id):
    session_check = check_session()
    if session_check:
        return session_check

    quiz = QuizService.get_quiz_by_id(quiz_id)
    return render_template("quiz_buzzer.html", quiz=quiz)

@quiz_bp.route("/quiz/<int:quiz_id>/update", methods=["POST"])
@login_required
def update_quiz(quiz_id):
    quiz = QuizService.get_quiz_by_id(quiz_id)
    if quiz.creator_id != current_user.id:
        flash("Vous n'êtes pas autorisé à modifier ce quiz.", "danger")
        return redirect(url_for("authentication.dashboard"))

    # Mettre à jour le titre du quiz
    quiz.title = request.form.get("title", "").strip()

    # Initialiser le dictionnaire pour stocker les nouveaux choix des nouvelles questions
    new_questions_choices = {}

    # Supprimer les questions marquées pour suppression
    removed_questions = request.form.get("remove_question[]", "").split(",")
    for question_id in removed_questions:
        if question_id.isdigit():
            question_to_delete = Question.query.get(int(question_id))
            if question_to_delete and question_to_delete.quiz_id == quiz.id:
                db.session.delete(question_to_delete)

    # Mise à jour des questions existantes
    for question in quiz.questions:
        new_text = request.form.get(f"question_{question.id}", "").strip()
        if new_text:
            question.text = new_text

        # Mise à jour des choix existants
        for choice in question.answers:
            choice_text_existing = request.form.get(
                f"choice_{question.id}_{choice.id}", ""
            ).strip()
            if choice_text_existing:
                choice.text = choice_text_existing

    # Ajout de nouvelles questions
    new_questions = {}
    for key, value in request.form.items():
        if key.startswith("new_question_") and value.strip():
            question_text = value.strip()
            new_question = Question(text=question_text, quiz_id=quiz.id)
            db.session.add(new_question)
            db.session.commit()
            new_questions[int(key.split("_")[2])] = new_question.id

    # Ajout des nouveaux choix aux questions existantes
    for key, value in request.form.items():
        if key.startswith("new_choice_"):
            parts = key.split("_")
            # Si le choix appartient à une question existante
            if len(parts) == 4 and parts[2].isdigit() and parts[3].isdigit():
                question_id = int(parts[2])
                choice_text = value.strip()

                if choice_text:
                    new_choice = Answer(text=choice_text, question_id=question_id)
                    db.session.add(new_choice)
                    db.session.commit()

            # Si le choix appartient à une nouvelle question
            elif (
                len(parts) == 5
                and parts[2] == "new"
                and parts[3].isdigit()
                and parts[4].isdigit()
            ):
                question_idx = int(parts[3])
                choice_text = value.strip()

                if choice_text:
                    if question_idx not in new_questions_choices:
                        new_questions_choices[question_idx] = []
                    new_questions_choices[question_idx].append(choice_text)

    db.session.commit()

    # Associer les choix aux nouvelles questions
    for question_idx, choices in new_questions_choices.items():
        new_question_id = new_questions[question_idx]

        for choice_text in choices:
            new_choice = Answer(text=choice_text, question_id=new_question_id)
            db.session.add(new_choice)

    db.session.commit()

    flash("Quiz mis à jour avec succès !", "success")
    return redirect(url_for("authentication.dashboard"))
