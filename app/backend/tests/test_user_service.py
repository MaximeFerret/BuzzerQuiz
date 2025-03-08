from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

import pytest
from backend.service.user_service import UserService


@pytest.fixture
def mock_user():
    """Fixture pour créer un utilisateur fictif"""

    class MockUser:
        """Mock pour un utilisateur"""

        def __init__(self, username, email, password_hash, is_host):
            self.username = username
            self.email = email
            self.password_hash = password_hash
            self.is_host = is_host

    return MockUser("testuser", "test@example.com", "hashed_password", False)


@patch("backend.dao.user_dao.UserDAO.create_user")
@patch("backend.service.user_service.bcrypt.generate_password_hash")
def test_create_user(mock_hash, mock_create_user, mock_user):
    """
    GIVEN un username, email, password et un statut d'hôte
    WHEN la méthode create_user est appelée
    THEN un utilisateur doit être créé et sauvegardé dans la base de données
    """
    mock_hash.return_value = "hashed_password"
    mock_create_user.return_value = mock_user

    user = UserService.create_user("testuser", "test@example.com", "password", False)

    assert user == mock_user
    mock_hash.assert_called_once_with("password")
    mock_create_user.assert_called_once_with(
        "testuser", "test@example.com", "hashed_password", False
    )


@patch("backend.dao.user_dao.UserDAO.get_user_by_email")
@patch("backend.service.user_service.bcrypt.check_password_hash")
def test_authenticate_user_success(mock_check_password, mock_get_user, mock_user):
    """
    GIVEN un email et un mot de passe valides
    WHEN authenticate_user est appelé
    THEN l'utilisateur doit être retourné
    """
    mock_get_user.return_value = mock_user
    mock_check_password.return_value = True

    user = UserService.authenticate_user("test@example.com", "password")

    assert user == mock_user
    mock_get_user.assert_called_once_with("test@example.com")
    mock_check_password.assert_called_once_with("hashed_password", "password")


@patch("backend.dao.user_dao.UserDAO.get_user_by_email")
@patch("backend.service.user_service.bcrypt.check_password_hash")
def test_authenticate_user_failure(mock_check_password, mock_get_user):
    """
    GIVEN un email inexistant ou un mot de passe incorrect
    WHEN authenticate_user est appelé
    THEN la méthode doit retourner None
    """
    mock_get_user.return_value = None
    user = UserService.authenticate_user("wrong@example.com", "password")
    assert user is None

    mock_get_user.return_value = MagicMock(password_hash="hashed_password")
    mock_check_password.return_value = False
    user = UserService.authenticate_user("test@example.com", "wrong_password")
    assert user is None


@patch("backend.dao.user_dao.UserDAO.get_user_by_email")
def test_get_user_by_email(mock_get_user, mock_user):
    """
    GIVEN un email existant
    WHEN get_user_by_email est appelé
    THEN l'utilisateur correspondant doit être retourné
    """
    mock_get_user.return_value = mock_user

    user = UserService.get_user_by_email("test@example.com")

    assert user == mock_user
    mock_get_user.assert_called_once_with("test@example.com")


def test_set_user_session():
    """
    GIVEN un ID utilisateur
    WHEN set_user_session est appelé
    THEN un dictionnaire de session utilisateur doit être retourné
    """
    user_id = 1
    session = UserService.set_user_session(user_id)

    assert session["is_user"] is True
    assert session["user_id"] == user_id
    assert isinstance(session["user_last_active"], datetime)


def test_set_admin_session():
    """
    GIVEN un administrateur
    WHEN set_admin_session est appelé
    THEN un dictionnaire de session admin doit être retourné
    """
    session = UserService.set_admin_session()

    assert session["is_admin"] is True
    assert isinstance(session["admin_last_active"], datetime)


def test_reset_user_session():
    """
    GIVEN une session utilisateur active
    WHEN reset_user_session est appelé
    THEN la session doit être réinitialisée
    """
    session = UserService.reset_user_session()

    assert session["is_user"] is None
    assert session["user_last_active"] is None


def test_reset_admin_session():
    """
    GIVEN une session admin active
    WHEN reset_admin_session est appelé
    THEN la session admin doit être réinitialisée
    """
    session = UserService.reset_admin_session()

    assert session["is_admin"] is None
    assert session["admin_last_active"] is None


@pytest.mark.parametrize(
    "last_active, timeout, expected",
    [
        (datetime.now(timezone.utc) - timedelta(minutes=5), 10, False),
        (datetime.now(timezone.utc) - timedelta(minutes=15), 10, True),
        (None, 10, True),  # Aucune activité => expiré
    ],
)
def test_check_session_expiry(last_active, timeout, expected):
    """
    GIVEN une dernière activité et un timeout
    WHEN check_session_expiry est appelé
    THEN il doit retourner True si la session est expirée, False sinon
    """
    result = UserService.check_session_expiry(last_active, timeout)
    assert result == expected
