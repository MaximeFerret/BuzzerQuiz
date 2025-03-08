import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI", "sqlite:///buzzerquiz.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_SECRET_CODE = os.getenv("ADMIN_SECRET_CODE", "admin123")
