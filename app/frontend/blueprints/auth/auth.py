from datetime import datetime, timedelta, timezone

from backend.models.db import db
from backend.models.user import User
from flask import (Blueprint, current_app, flash, redirect, render_template,
                   request, session, url_for)
from flask_login import current_user, login_required, login_user, logout_user

auth_bp = Blueprint("authentication", __name__, template_folder="templates")


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

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Cet email est déjà utilisé.", "danger")
            return redirect(url_for("authentication.register"))

        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            flash("Ce nom d'utilisateur est déjà utilisé.", "danger")
            return redirect(url_for("authentication.register"))

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        # flash("Compte créé avec succès ! Connectez-vous.", "success")
        return redirect(url_for("authentication.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("is_user") and "user_last_active" in session:
        last_active = session.get("user_last_active")
        if datetime.now(timezone.utc) - last_active <= timedelta(minutes=10):
            return redirect(url_for("authentication.dashboard"))
        else:
            # Si l'inactivité dépasse la limite, on le déconnecte
            session.pop("is_user", None)
            session.pop("user_last_active", None)
            flash("Session expirée. Veuillez vous reconnecter.", "warning")
            return redirect(url_for("authentication.login"))

    # if current_user.is_authenticated:
    #    return redirect(url_for('authentication.dashboard'))

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            session["is_user"] = True  # ✅ On stocke l'info dans la session
            session["user_last_active"] = datetime.now(timezone.utc)
            # flash("Connexion réussie !", "success")
            return redirect(url_for("authentication.dashboard"))
        else:
            flash("Email ou mot de passe incorrect.", "danger")
            return redirect(url_for("authentication.login"))

    return render_template("login.html")


@auth_bp.route("/dashboard")
@login_required
def dashboard():
    if not session.get("is_user") or "user_last_active" not in session:
        return redirect(url_for("authentication.login"))

    # Vérifie le temps d'inactivité
    last_active = session.get("user_last_active")
    if datetime.now(timezone.utc) - last_active > timedelta(
        minutes=10
    ):  # Déconnecte après 10 minutes
        session.pop("is_user", None)
        session.pop("user_last_active", None)
        flash("Session expirée. Veuillez vous reconnecter.", "warning")
        return redirect(url_for("authentication.login"))

    # Met à jour le dernier moment d'activité
    session["user_last_active"] = datetime.now(timezone.utc)

    return render_template("dashboard.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    session.pop("is_user", None)
    session.pop("user_last_active", None)
    return redirect(url_for("authentication.login"))


@auth_bp.route("/admin", methods=["GET", "POST"])
def admin():
    print(session.get("is_admin"))
    if session.get("is_admin") and "admin_last_active" in session:
        last_active = session.get("admin_last_active")
        # Vérifie si la session admin est encore valide (en vérifiant l'inactivité)
        if datetime.now(timezone.utc) - last_active <= timedelta(minutes=10):
            return redirect(
                url_for("authentication.admin_dashboard")
            )  # Redirige directement vers le dashboard
        else:
            # Si l'inactivité dépasse la limite, on le déconnecte
            session.pop("is_admin", None)
            session.pop("admin_last_active", None)
            flash("Session expirée. Veuillez vous reconnecter.", "warning")
            return redirect(url_for("authentication.admin"))

    if request.method == "POST":
        secret_code = request.form["secret_code"]

        # Vérifie si le code correspond à celui défini dans la config Flask
        if secret_code == current_app.config["ADMIN_SECRET_CODE"]:
            session["is_admin"] = True  # ✅ On stocke l'info dans la session
            session["admin_last_active"] = datetime.now(timezone.utc)
            flash("Accès administrateur accordé.", "success")
            return redirect(url_for("authentication.admin_dashboard"))
        else:
            flash("Code incorrect. Accès refusé.", "danger")
    return render_template(
        "admin_login.html"
    )  # 🔥 Un formulaire HTML pour entrer le code


@auth_bp.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("is_admin") or "admin_last_active" not in session:
        flash("Veuillez entrer le code administrateur.", "danger")
        return redirect(url_for("authentication.admin"))

    # Vérifie le temps d'inactivité
    last_active = session.get("admin_last_active")
    if datetime.now(timezone.utc) - last_active > timedelta(
        minutes=10
    ):  # Déconnecte après 10 minutes
        session.pop("is_admin", None)
        session.pop("admin_last_active", None)
        flash("Session expirée. Veuillez vous reconnecter.", "warning")
        return redirect(url_for("authentication.admin"))

    # Met à jour le dernier moment d'activité
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
    session.pop("is_admin", None)
    session.pop("admin_last_active", None)
    return redirect(url_for("authentication.admin"))
