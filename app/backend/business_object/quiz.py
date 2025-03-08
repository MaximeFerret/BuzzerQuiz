from ..business_object.db import db


class Quiz(db.Model):
    """
    Classe représentant un quiz.

    Cette classe représente un quiz avec ses questions et ses réponses.

    Attributes:
    -----------
        id (int): l'identifiant du quiz.
        title (str): le titre du quiz.
        code (str): le code du quiz.
        creator_id (int): l'identifiant de l'utilisateur qui a créé le quiz.
        questions (list): les questions du quiz.
        is_active (bool): si le quiz est actif.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(6), unique=True, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                           nullable=False)
    questions = db.relationship('Question', backref='quiz', lazy=True)
    is_active = db.Column(db.Boolean, default=False)


class Question(db.Model):
    """
    Classe représentant une question d'un quiz.

    Cette classe représente une question d'un quiz avec ses options et sa
    réponse.

    Attributes:
    -----------
        id (int): l'identifiant de la question.
        quiz_id (int): l'identifiant du quiz auquel appartient la question.
        question_text (str): le texte de la question.
        has_choices (bool): si la question a des options.
        option1 (str): la première option de la question.
        option2 (str): la deuxième option de la question.
        option3 (str): la troisième option de la question.
        option4 (str): la quatrième option de la question.
        correct_answer (int): la réponse correcte de la question.
    """
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question_text = db.Column(db.String(500), nullable=False)
    has_choices = db.Column(db.Boolean, nullable=False, default=True)
    option1 = db.Column(db.String(200), nullable=True)
    option2 = db.Column(db.String(200), nullable=True)
    option3 = db.Column(db.String(200), nullable=True)
    option4 = db.Column(db.String(200), nullable=True)
    correct_answer = db.Column(db.Integer, nullable=True)
