import re
from datetime import datetime, timezone

from backend.business_object.db import db
from backend.business_object.user import User
from backend.service.user_service import UserService
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import login_required, login_user, logout_user


def is_valid_email(email):
    """Vérifie si une adresse email est valide.

    Cette fonction utilise une expression régulière pour valider le format
    d'une adresse email.

    Parameters:
    -----------
        email (str): l'email à vérifier.

    Return:
    -------
        bool: True si l'email est valide, False sinon.
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def is_valid_password(password):
    """Vérifie si un mot de passe est valide.

    Cette fonction vérifie si le mot de passe contient au moins 8 caractères,
    une majuscule, une minuscule et un caractère spécial.

    Parameters:
    -----------
        password (str): le mot de passe à vérifier.

    Return:
    -------
        bool: True si le mot de passe est valide, False sinon.
    """

    if len(password) < 8:
        return False, "Le mot de passe doit contenir au moins 8 caractères."
    if not re.search(r"[A-Z]", password):
        return False, "Le mot de passe doit contenir au moins une majuscule."
    if not re.search(r"[a-z]", password):
        return False, "Le mot de passe doit contenir au moins une minuscule."
    if not re.search(r"\d", password):
        return False, "Le mot de passe doit contenir au moins un chiffre."
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return (False, "Le mot de passe doit contenir au moins un caractère spécial.")
    return True, ""


auth_bp = Blueprint("authentication", __name__, template_folder="../../frontend/user")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Route pour l'inscription d'un utilisateur.

    Cette route permet à un utilisateur de s'inscrire à l'application.
    Elle gère les requêtes GET et POST.

    Return:
    -------
        str: le template HTML pour l'inscription.
    """
    if request.method == "GET":
        return render_template("register.html")

    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    confirm_password = request.form["confirm_password"]
    is_host = request.form.get("is_host") == "on"

    if not is_valid_email(email):
        flash("L'adresse email n'est pas valide.", "danger")
        return redirect(url_for("authentication.register"))

    is_password_valid, password_error = is_valid_password(password)
    if not is_password_valid:
        flash(password_error, "danger")
        return redirect(url_for("authentication.register"))

    if password != confirm_password:
        flash("Les mots de passe ne correspondent pas.", "danger")
        return redirect(url_for("authentication.register"))

    if UserService.get_user_by_email(email):
        flash("Cet email est déjà utilisé.", "danger")
        return redirect(url_for("authentication.register"))

    if UserService.get_user_by_username(username):
        flash("Cet username est déjà utilisé.", "danger")
        return redirect(url_for("authentication.register"))

    UserService.create_user(username, email, password, is_host)
    flash("Compte créé avec succès ! Connectez-vous.", "success")
    return redirect(url_for("authentication.login"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Route pour la connexion d'un utilisateur.

    Cette route permet à un utilisateur de se connecter à l'application.
    Elle gère les requêtes GET et POST.

    Return:
    -------
        str: le template HTML pour la connexion.
    """
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if user := UserService.authenticate_user(email, password):
            login_user(user)
            session.update(UserService.set_user_session(user.id))
            return redirect(url_for("quiz.dashboard"))
        else:
            flash("Email ou mot de passe incorrect.", "danger")
            return redirect(url_for("authentication.login"))
    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    """Route pour la déconnexion d'un utilisateur.

    Cette route permet à un utilisateur de se déconnecter de l'application.
    Elle gère les requêtes GET et POST.

    Return:
    -------
        str: le template HTML pour la déconnexion.
    """
    logout_user()
    session.update(UserService.reset_user_session())
    return redirect(url_for("authentication.login"))


@auth_bp.route("/admin", methods=["GET", "POST"])
def admin():
    """Route pour la connexion administrateur.

    Cette route permet à un administrateur de se connecter à l'application.
    Elle gère les requêtes GET et POST.

    Return:
    -------
        str: le template HTML pour la connexion administrateur.
    """
    if request.method == "POST":
        secret_code = request.form["secret_code"]
        if secret_code == current_app.config["ADMIN_SECRET_CODE"]:
            session.update(UserService.set_admin_session())
            return redirect(url_for("authentication.admin_dashboard"))
        else:
            flash("Code incorrect. Accès refusé.", "danger")
            return redirect(url_for("authentication.admin"))

    return render_template("admin_login.html")


@auth_bp.route("/admin/dashboard")
def admin_dashboard():
    """Route pour le tableau de bord administrateur.

    Cette route permet à un administrateur de voir le tableau de bord de
    l'application.
    Elle gère les requêtes GET et POST.

    Return:
    -------
        str: le template HTML pour le tableau de bord administrateur.
    """

    last_active = session.get("admin_last_active")
    if UserService.check_session_expiry(last_active):
        flash("Session expirée. Veuillez vous reconnecter.", "warning")
        return redirect(url_for("authentication.admin"))

    session["admin_last_active"] = datetime.now(timezone.utc)
    users = User.query.all()
    return render_template("admin_dashboard.html", users=users)


@auth_bp.route("/admin/delete_user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    """Route pour la suppression d'un utilisateur.

    Cette route permet à un administrateur de supprimer un utilisateur de
    l'application.
    Elle gère les requêtes GET et POST.

    Return:
    -------
        str: le template HTML pour la suppression d'un utilisateur.
    """
    if user := User.query.get(user_id):
        db.session.delete(user)
        db.session.commit()
        flash("Utilisateur supprimé avec succès.", "success")
    return redirect(url_for("authentication.admin_dashboard"))


@auth_bp.route("/admin_logout")
def admin_logout():
    """Route pour la déconnexion administrateur.

    Cette route permet à un administrateur de se déconnecter de l'application.
    Elle gère les requêtes GET et POST.

    Return:
    -------
        str: le template HTML pour la déconnexion administrateur.
    """
    session.update(UserService.reset_admin_session())
    return redirect(url_for("authentication.admin"))
