class Config:
    SECRET_KEY = "EnsaiBruz35170!"  # Change cette clé pour plus de sécurité
    SQLALCHEMY_DATABASE_URI = "sqlite:///buzzerquiz.db"  # Base de données SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_SECRET_CODE = "admin123"
