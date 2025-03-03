from flask import (Blueprint, current_app, flash, redirect, render_template,
                   request, session, url_for)
from flask_login import current_user, login_required, login_user, logout_user
from backend.models.db import db
from backend.models.user import User
from backend.services.auth_service import AuthService
from datetime import datetime, timezone, timedelta

auth_bp = Blueprint("authentication", __name__, template_folder="../../frontend/blueprints/auth/templates")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            flash("Les mots de passe ne correspondent pas.", "danger")
            return redirect(url_for("authentication.register"))

        if AuthService.get_user_by_email(email):
            flash("Cet email est déjà utilisé.", "danger")
            return redirect(url_for("authentication.register"))

        new_user = AuthService.create_user(username, email, password)
        flash("Compte créé avec succès ! Connectez-vous.", "success")
        return redirect(url_for("authentication.login"))
    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = AuthService.authenticate_user(email, password)
        if user:
            login_user(user)
            session.update(AuthService.set_user_session(user.id))
            return redirect(url_for("authentication.dashboard"))
        else:
            flash("Email ou mot de passe incorrect.", "danger")
            return redirect(url_for("authentication.login"))
    return render_template("login.html")

@auth_bp.route("/dashboard")
@login_required
def dashboard():
    if not session.get("is_user"):
        return redirect(url_for("authentication.login"))

    last_active = session.get("user_last_active")
    if AuthService.check_session_expiry(last_active):
        flash("Session expirée. Veuillez vous reconnecter.", "warning")
        return redirect(url_for("authentication.login"))
    
    session["user_last_active"] = datetime.now(timezone.utc)
    return render_template("dashboard.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    session.update(AuthService.reset_user_session())
    return redirect(url_for("authentication.login"))

@auth_bp.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        secret_code = request.form["secret_code"]
        if secret_code == current_app.config["ADMIN_SECRET_CODE"]:
            session.update(AuthService.set_admin_session())
            return redirect(url_for("authentication.admin_dashboard"))
        else:
            flash("Code incorrect. Accès refusé.", "danger")
            return redirect(url_for("authentication.admin"))

    return render_template("admin_login.html")

@auth_bp.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("is_admin"):
        flash("Veuillez entrer le code administrateur.", "danger")
        return redirect(url_for("authentication.admin"))

    last_active = session.get("admin_last_active")
    if AuthService.check_session_expiry(last_active):
        flash("Session expirée. Veuillez vous reconnecter.", "warning")
        return redirect(url_for("authentication.admin"))

    session["admin_last_active"] = datetime.now(timezone.utc)
    users = User.query.all()
    return render_template("admin_dashboard.html", users=users)

@auth_bp.route("/admin/delete_user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    if not session.get("is_admin"):
        flash("Accès refusé.", "danger")
        return redirect(url_for("authentication.admin"))

    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash("Utilisateur supprimé avec succès.", "success")
    return redirect(url_for("authentication.admin_dashboard"))

@auth_bp.route("/admin_logout")
def admin_logout():
    session.update(AuthService.reset_admin_session())
    return redirect(url_for("authentication.admin"))
