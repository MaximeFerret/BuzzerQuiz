from ..business_object.db import db
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

bcrypt = Bcrypt()


class User(db.Model, UserMixin):
    """
    Classe représentant un utilisateur.

    Cette classe représente un utilisateur avec son nom d'utilisateur,
    son email, son mot de passe et si c'est un hôte ou non.

    Attributes:
    -----------
        id (int): l'identifiant de l'utilisateur.
        username (str): le nom d'utilisateur de l'utilisateur.
        email (str): l'email de l'utilisateur.
        password_hash (str): le mot de passe de l'utilisateur.
        is_host (bool): si l'utilisateur est un hôte ou non.
        quizzes (list): les quizzes créés par l'utilisateur.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_host = db.Column(db.Boolean, default=False)
    quizzes = db.relationship('Quiz', backref='creator', lazy=True)

    def set_password(self, password):
        """
        Définit le mot de passe de l'utilisateur.

        Cette méthode permet de définir le mot de passe de l'utilisateur.
        """
        hashed = bcrypt.generate_password_hash(password)
        self.password_hash = hashed.decode("utf-8")

    def check_password(self, password):
        """
        Vérifie si le mot de passe est correct.

        Cette méthode permet de vérifier si le mot de passe est correct.
        """
        return bcrypt.check_password_hash(self.password_hash, password)
