import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "default_secret_key")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "SQLALCHEMY_DATABASE_URI", "sqlite:///buzzerquiz.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_SECRET_CODE = os.environ.get("ADMIN_SECRET_CODE", "admin123")
