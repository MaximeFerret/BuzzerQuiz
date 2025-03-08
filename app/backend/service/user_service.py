from datetime import datetime, timedelta, timezone

from flask_bcrypt import Bcrypt

from ..dao.user_dao import UserDAO

bcrypt = Bcrypt()


class UserService:
    """
    Service pour les opérations liées aux utilisateurs.
    """

    @staticmethod
    def create_user(username, email, password, is_host):
        """Création de l'utilisateur et sauvgarder

        Cette méthode permet de créer un utilisateur et de le sauvegarder
        dans la base de données.

        Parameters:
        -----------
            username (str): le nom d'utilisateur de l'utilisateur.
            email (str): l'email de l'utilisateur.
            password (str): le mot de passe de l'utilisateur.
            is_host (bool): si l'utilisateur est un hôte ou non.

        Return:
        -------
            User: l'utilisateur créé.
        """
        password_hash = bcrypt.generate_password_hash(password)
        return UserDAO.create_user(username, email, password_hash, is_host)

    @staticmethod
    def authenticate_user(email, password):
        """Authentification de l'utilisateur

        Cette méthode permet d'authentifier un utilisateur en vérifiant
        son email et son mot de passe.

        Parameters:
        -----------
            email (str): l'email de l'utilisateur.
            password (str): le mot de passe de l'utilisateur.
        """
        user = UserDAO.get_user_by_email(email)

        if not user or not bcrypt.check_password_hash(user.password_hash, password):
            return None

        return user

    @staticmethod
    def get_user_by_email(email):
        """Trouver l'utilisateur via email

        Cette méthode permet de trouver un utilisateur via son email.

        Parameters:
        -----------
            email (str): l'email de l'utilisateur.
        """
        return UserDAO.get_user_by_email(email)

    @staticmethod
    def get_user_by_username(id):
        """Trouver l'utilisateur via identifiant

        Cette méthode permet de trouver un utilisateur via son identifiant.

        Parameters:
        -----------
            id (int): l'identifiant de l'utilisateur.
        """
        return UserDAO.get_user_by_username(id)

    @staticmethod
    def set_user_session(user_id):
        """Configurer la session de l'utilisateur

        Cette méthode permet de configurer la session de l'utilisateur.

        Parameters:
        -----------
            user_id (int): l'identifiant de l'utilisateur.
        """
        return {
            "is_user": True,
            "user_last_active": datetime.now(timezone.utc),
            "user_id": user_id,
        }

    @staticmethod
    def set_admin_session():
        """Configurer la session de l'admin

        Cette méthode permet de configurer la session de l'admin.

        Return:
        -------
            dict: la session de l'admin.
        """
        return {"is_admin": True, "admin_last_active": datetime.now(timezone.utc)}

    @staticmethod
    def reset_user_session():
        """Réinitialiser la session de l'utilisateur

        Cette méthode permet de réinitialiser la session de l'utilisateur.

        Return:
        -------
            dict: la session de l'utilisateur.
        """
        return {"is_user": None, "user_last_active": None}

    @staticmethod
    def reset_admin_session():
        """Réinitialiser la session de l'admin

        Cette méthode permet de réinitialiser la session de l'admin.

        Return:
        -------
            dict: la session de l'admin.
        """
        return {"is_admin": None, "admin_last_active": None}

    @staticmethod
    def check_session_expiry(last_active, timeout=10):
        """Vérifier si la session est expirée

        Cette méthode permet de vérifier si la session est expirée.

        Parameters:
        -----------
            last_active (datetime): la date de dernière activité de
                l'utilisateur.
            timeout (int): le temps de déconnexion de l'utilisateur. Par
                défaut, il est de 10 minutes.

        Return:
        -------
            bool: True si la session est expirée, False sinon.
        """
        if not last_active:
            return True
        now = datetime.now(timezone.utc)
        return now - last_active > timedelta(minutes=timeout)
