from app.backend.models.user import User
from app.backend.models import db
from datetime import datetime, timezone

class UserDAO:
    @staticmethod
    def create_user(username, email, password_hash):
        """Créer un user"""
        new_user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def get_user_by_email(email):
        """Obtenir un user par mail"""
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_user_by_id(user_id):
        """Obtenir un user par id"""
        return User.query.get(user_id)

    @staticmethod
    def delete_user(user_id):
        """Supprimer un user"""
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False