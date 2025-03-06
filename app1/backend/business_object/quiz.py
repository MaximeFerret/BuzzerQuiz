from backend.business_object.db import db


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(6), unique=True, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    questions = db.relationship('Question', backref='quiz', lazy=True)
    is_active = db.Column(db.Boolean, default=False)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question_text = db.Column(db.String(500), nullable=False)
    has_choices = db.Column(db.Boolean, nullable=False, default=True)
    option1 = db.Column(db.String(200), nullable=True)
    option2 = db.Column(db.String(200), nullable=True)
    option3 = db.Column(db.String(200), nullable=True)
    option4 = db.Column(db.String(200), nullable=True)
    correct_answer = db.Column(db.Integer, nullable=True)
