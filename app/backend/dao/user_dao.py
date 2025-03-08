from ..business_object.db import db
from ..business_object.user import User


class UserDAO:
    @staticmethod
    def create_user(username, email, password_hash, is_host):
        """Créer un user.

        Cette méthode permet de créer un user.

        Parameters:
        -----------
            username (str): le nom d'utilisateur.
            email (str): l'adresse email.
            password_hash (str): le hash du mot de passe.
            is_host (bool): si l'utilisateur est un hôte.

        Returns:
        --------
            User: le user créé.
        """
        try:

            new_user = User(
                username=username,
                email=email,
                password_hash=password_hash,
                is_host=is_host,
            )
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except Exception as e:
            db.session.rollback()
            print(f"Erreur lors de la création de l'utilisateur : {e}")
            return None

    @staticmethod
    def get_user_by_email(email):
        """Obtenir un user par mail.

        Cette méthode permet d'obtenir un user par mail.

        Parameters:
        -----------
            email (str): l'adresse email.

        Returns:
        --------
            User: le user obtenu.
        """
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_user_by_username(username):
        """Obtenir un user par username.

        Cette méthode permet d'obtenir un user par username.

        Parameters:
        -----------
            username (str): le nom d'utilisateur.

        Returns:
        --------
            User: le user obtenu.
        """
        return User.query.filter_by(username=username).first()

    @staticmethod
    def delete_user(user_id):
        """Supprimer un user.

        Cette méthode permet de supprimer un user.

        Parameters:
        -----------
            user_id (int): l'ID du user.

        Returns:
        --------
            bool: True si le user a été supprimé, False sinon.
        """
        try:
            if user := User.query.get(user_id):
                db.session.delete(user)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            msg = f"Erreur lors de la suppression de l'utilisateur {user_id}"
            print(f"{msg} : {e}")
            return False

    @staticmethod
    def update_user(user_id, **kwargs):
        """Met à jour un utilisateur avec les champs donnés.

        Cette méthode permet de mettre à jour un utilisateur avec les champs
        donnés.

        Parameters:
        -----------
            user_id (int): l'ID du user.
            **kwargs: les champs à mettre à jour.

        Returns:
        --------
            User: le user mis à jour.
        """
        try:
            if user := User.query.get(user_id):
                for key, value in kwargs.items():
                    setattr(user, key, value)
                db.session.commit()
                return user
            return None
        except Exception as e:
            db.session.rollback()
            msg = f"Erreur lors de la mise à jour de l'utilisateur {user_id}"
            print(f"{msg} : {e}")
            return None
