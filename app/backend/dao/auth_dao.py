from datetime import datetime, timezone

from backend.models.db import db
from backend.models.user import User


class UserDAO:
    @staticmethod
    def create_user(username, email, password_hash):
        """Créer un user"""
        try:

            new_user = User(username=username, email=email, password_hash=password_hash)
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except Exception as e:
            db.session.rollback()
            print(f"Erreur lors de la création de l'utilisateur : {e}")
            return None

    @staticmethod
    def get_user_by_email(email):
        """Obtenir un user par mail"""
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_user_by_username(username):
        """Obtenir un user par username"""
        return User.query.filter_by(username=username).first()

    @staticmethod
    def delete_user(user_id):
        """Supprimer un user"""
        try:

            user = User.query.get(user_id)
            if user:
                db.session.delete(user)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            print(f"Erreur lors de la suppression de l'utilisateur {user_id} : {e}")
            return False

    @staticmethod
    def update_user(user_id, **kwargs):
        """Met à jour un utilisateur avec les champs donnés"""
        try:
            user = User.query.filter_by(id=user_id).first()
            if not user:
                return None
            for key, value in kwargs.items():
                setattr(user, key, value)
                db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            print(f"Erreur lors de la mise à jour de l'utilisateur : {e}")
            return None
