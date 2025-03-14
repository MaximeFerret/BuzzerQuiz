from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from ..business_object.db import db
from ..service.quiz_service import QuizService

quiz_bp = Blueprint("quiz", __name__, template_folder="../../frontend/quiz")

# Stockage des joueurs et de leurs scores en mémoire
players = {}
active_quizzes = {}


@quiz_bp.route("/dashboard")
@login_required
def dashboard():
    if current_user.is_host:
        quizzes = QuizService.get_quizzes_by_creator_id(current_user.id)
    else:
        quizzes = []
    return render_template("dashboard.html", quizzes=quizzes)


@quiz_bp.route("/create_quiz", methods=["GET", "POST"])
@login_required
def create_quiz():
    """Route pour la création d'un quiz.

    Cette route permet à un utilisateur de créer un quiz.
    Elle gère les requêtes GET et POST.

    Return:
    -------
        str: le template HTML pour la création d'un quiz.
    """
    if request.method == "POST":
        try:
            title = request.form.get("title")
            quiz = QuizService.create_quiz(title, current_user.id)

            # Récupérer toutes les questions du formulaire
            i = 1
            while f"question{i}" in request.form:
                question_text = request.form.get(f"question{i}")
                has_choices = f"correct{i}" in request.form

                if has_choices:
                    correct_answer = int(request.form.get(f"correct{i}")) - 1
                    options = []
                    j = 1
                    while f"option{j}_{i}" in request.form:
                        options.append(request.form.get(f"option{j}_{i}"))
                        j += 1
                else:
                    correct_answer = None
                    options = [None] * 4

                if question_text:
                    QuizService.add_question_to_quiz(
                        quiz.id, question_text, has_choices, options, correct_answer
                    )
                i += 1

            flash("Quiz créé avec succès!")
            return redirect(url_for("quiz.dashboard"))
        except Exception as e:
            flash(f"Erreur lors de la création du quiz: {str(e)}")
            return redirect(url_for("quiz.create_quiz"))

    return render_template("create_quiz.html")


@quiz_bp.route("/edit_quiz/<int:quiz_id>", methods=["GET", "POST"])
@login_required
def edit_quiz(quiz_id):
    """Route pour la modification d'un quiz.

    Cette route permet à un utilisateur de modifier un quiz.
    Elle gère les requêtes GET et POST.

    Return:
    -------
        str: le template HTML pour la modification d'un quiz.
    """
    quiz = QuizService.get_quiz_by_id(quiz_id)
    # Vérifier que l'utilisateur est le propriétaire du quiz
    if quiz.creator_id != current_user.id:
        flash("Vous n'êtes pas autorisé à modifier ce quiz")
        return redirect(url_for("quiz.dashboard"))

    if request.method == "POST":
        try:
            quiz.title = request.form.get("title")

            # Supprimer les anciennes questions
            QuizService.delete_questions_by_quiz_id(quiz.id)

            # Ajouter les nouvelles questions
            i = 1
            while f"question{i}" in request.form:
                question_text = request.form.get(f"question{i}")
                has_choices = request.form.get(f"has_choices{i}") == "on"

                if has_choices:
                    answer_key = f"correct_answer_{i}"
                    correct_answer = int(request.form.get(answer_key))
                    options = []
                    j = 1
                    while f"option{j}_{i}" in request.form:
                        options.append(request.form.get(f"option{j}_{i}"))
                        j += 1
                else:
                    correct_answer = None
                    options = [None] * 4

                if question_text:
                    QuizService.add_question_to_quiz(
                        quiz.id, question_text, has_choices, options, correct_answer
                    )
                i += 1

            flash("Quiz modifié avec succès!")
            return redirect(url_for("quiz.dashboard"))
        except Exception as e:
            flash(f"Erreur lors de la modification du quiz: {str(e)}")
            return redirect(url_for("quiz.edit_quiz", quiz_id=quiz_id))

    questions = QuizService.get_questions_by_quiz_id(quiz.id)
    return render_template("edit_quiz.html", quiz=quiz, questions=questions)


@quiz_bp.route("/delete_quiz/<int:quiz_id>", methods=["POST"])
@login_required
def delete_quiz(quiz_id):
    """Route pour la suppression d'un quiz.

    Cette route permet à un utilisateur de supprimer un quiz.
    Elle gère les requêtes GET et POST.

    Return:
    -------
        str: le template HTML pour la suppression d'un quiz.
    """
    quiz = QuizService.get_quiz_by_id(quiz_id)
    try:
        QuizService.delete_quiz(quiz)
        flash("Quiz supprimé avec succès!")
    except Exception as e:
        flash(f"Erreur lors de la suppression du quiz: {str(e)}")

    return redirect(url_for("quiz.dashboard"))


@quiz_bp.route("/reactivate_quiz", methods=["POST"])
def reactivate_quiz():
    """Route pour la réactivation d'un quiz.

    Cette route permet à un utilisateur de réactiver un quiz.
    Elle gère les requêtes GET et POST.

    Return:
    -------
        str: le template HTML pour la réactivation d'un quiz.
    """
    data = request.get_json()
    code = data.get("code")
    quiz = QuizService.get_quiz_by_code(code)

    if not quiz or quiz.creator_id != current_user.id:
        return jsonify({"success": False, "message": "Quiz non trouvé ou non autorisé"})

    quiz.is_active = True
    db.session.commit()
    return jsonify({"success": True})


@quiz_bp.route("/start_quiz", methods=["POST"])
@login_required
def start_quiz():
    """Route pour le démarrage d'un quiz.

    Cette route permet à un utilisateur de démarrer un quiz.
    Elle gère les requêtes GET et POST.

    Return:
    -------
        str: le template HTML pour le démarrage d'un quiz.
    """
    data = request.get_json()
    code = data.get("code")
    quiz = QuizService.get_quiz_by_code(code)

    if not quiz or quiz.creator_id != current_user.id:
        return jsonify({"success": False, "message": "Quiz non trouvé ou non autorisé"})

    # Nettoyer les données de la session précédente
    if code in active_quizzes:
        del active_quizzes[code]
    # Supprimer les scores des joueurs de cette partie
    for username, player_data in list(players.items()):
        if player_data["room"] == code:
            del players[username]

    quiz.is_active = True
    db.session.commit()
    return jsonify({"success": True})


@quiz_bp.route("/stop_quiz", methods=["POST"])
@login_required
def stop_quiz():
    """Route pour l'arrêt d'un quiz.

    Cette route permet à un utilisateur de stopper un quiz.
    Elle gère les requêtes GET et POST.

    Return:
    -------
        str: le template HTML pour l'arrêt d'un quiz.
    """
    data = request.get_json()
    code = data.get("code")
    quiz = QuizService.get_quiz_by_code(code)

    if not quiz or quiz.creator_id != current_user.id:
        return jsonify({"success": False, "message": "Quiz non trouvé ou non autorisé"})

    quiz.is_active = False
    db.session.commit()

    # Nettoyer les données de la partie en cours
    if code in active_quizzes:
        del active_quizzes[code]
        # Supprimer les scores des joueurs de cette partie
        for username, player_data in list(players.items()):
            if player_data["room"] == code:
                del players[username]

    return jsonify({"success": True})


@quiz_bp.route("/waiting_room/<code>")
@login_required
def waiting_room(code):
    """Route pour la salle d'attente d'un quiz.

    Cette route permet à un utilisateur de se connecter à la salle d'attente
    d'un quiz.
    Elle gère les requêtes GET et POST.

    Return:
    -------
        str: le template HTML pour la salle d'attente d'un quiz.
    """
    quiz = QuizService.get_quiz_by_code(code)
    return render_template("waiting_room.html", quiz=quiz)


@quiz_bp.route("/quiz/<code>")
@login_required
def quiz_page(code):
    """Route pour la page du quiz.

    Cette route permet à un utilisateur de se connecter à la page du quiz.
    Elle gère les requêtes GET et POST.

    Return:
    -------
        str: le template HTML pour la page du quiz.
    """
    quiz = QuizService.get_quiz_by_code(code)
    questions = QuizService.get_questions_by_quiz_id(quiz.id)
    if not questions:
        flash("Ce quiz ne contient aucune question")
        return redirect(url_for("quiz.dashboard"))
    return render_template("quiz_page.html", quiz=quiz, questions=questions)


@quiz_bp.route("/join/<code>")
def join_game(code):
    """Route pour la jointure d'un quiz.

    Cette route permet à un utilisateur de se connecter à un quiz.
    Elle gère les requêtes GET et POST.

    Return:
    -------
        str: le template HTML pour la jointure d'un quiz.
    """
    quiz = QuizService.get_quiz_by_code(code)
    if not quiz:
        flash("Code de quiz invalide")
        return redirect(url_for("homepage"))
    return render_template("join_game.html", code=code)


@quiz_bp.route("/play/<code>")
def play_game(code):
    """Route pour la partie d'un quiz.

    Cette route permet à un utilisateur de se connecter à une partie d'un quiz.
    Elle gère les requêtes GET et POST.

    Return:
    -------
        str: le template HTML pour la partie d'un quiz.
    """
    quiz = QuizService.get_quiz_by_code(code)
    if not quiz.is_active:
        flash("Cette partie n'est pas active")
        return redirect(url_for("homepage"))
    return render_template("play_game.html", code=code)
