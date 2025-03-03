from datetime import datetime, timedelta, timezone

from backend.dao.auth_dao import UserDAO
from backend.models.db import db
from flask_login import login_user
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


class AuthService:
    @staticmethod
    def create_user(username, email, password):
        """Création de l'utilisateur et sauvgarder"""
        password_hash = bcrypt.generate_password_hash(password)
        new_user = UserDAO.create_user(username, email, password_hash)
        return new_user

    @staticmethod
    def authenticate_user(email, password):
        """L'authentification de l'utilisateur"""
        user = UserDAO.get_user_by_email(email)

        if not user or not bcrypt.check_password_hash(user.password_hash, password):
            return None

        return user
    
    @staticmethod
    def get_user_by_email(email):
        """Trouver l'utilisateur via email"""
        return UserDAO.get_user_by_email(email)

    @staticmethod
    def set_user_session(user_id):
        """Configurer la session de l'utilisateur"""
        return {
            "is_user": True,
            "user_last_active": datetime.now(timezone.utc),
            "user_id": user_id,
        }

    @staticmethod
    def set_admin_session():
        """Configurer la session de l'admin"""
        return {"is_admin": True, "admin_last_active": datetime.now(timezone.utc)}

    @staticmethod
    def reset_user_session():
        """Réinitialiser la session de l'utilisateur"""
        return {"is_user": None, "user_last_active": None}

    @staticmethod
    def reset_admin_session():
        """Réinitialiser la session de l'admin"""
        return {"is_admin": None, "admin_last_active": None}

    @staticmethod
    def check_session_expiry(last_active, timeout=10):
        """Vérifier si la session est expirée"""
        if not last_active:
            return True
        return datetime.now(timezone.utc) - last_active > timedelta(minutes=timeout)
