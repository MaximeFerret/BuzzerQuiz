# pour tester executer pytest -v app/backend/tests/
import os
import sys
from unittest.mock import MagicMock

import pytest

# Ajoute le dossier racine du projet (BuzzerQuiz) dans sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from backend.services.auth_service import AuthService
from werkzeug.security import check_password_hash


@pytest.fixture
def new_user():
    """Créer un utilisateur fictif en tant qu'objet simulé"""
    user = MagicMock()
    user.id = 1
    user.username = "testuser"
    user.email = "test@example.com"
    user.password_hash = "hashed_password"
    return user


def test_create_user(mocker, new_user):
    """Test de création d'un utilisateur sans base de données"""
    mock_create = mocker.patch(
        "backend.dao.auth_dao.UserDAO.create_user", return_value=new_user
    )

    user = AuthService.create_user(new_user.username, new_user.email, "password123")

    mock_create.assert_called_once()  # Vérifie que la fonction a bien été appelée
    assert (
        user.email == new_user.email
    )  # 🔹 Correction : accès à l'attribut directement


def test_authenticate_user(mocker, new_user):
    """Test de l'authentification d'un utilisateur"""
    mock_get_user = mocker.patch(
        "backend.dao.auth_dao.UserDAO.get_user_by_email", return_value=new_user
    )

    #  S'assurer que new_user.password_hash est une vraie chaîne de caractères
    new_user.password_hash = "hashed_password"

    #  Simuler correctement la vérification du mot de passe
    mock_check_password = mocker.patch(
        "backend.services.auth_service.check_password_hash", return_value=True
    )

    user = AuthService.authenticate_user(new_user.email, "password123")

    mock_get_user.assert_called_once_with(new_user.email)  # Vérifie l'appel à la DAO
    mock_check_password.assert_called_once_with(
        new_user.password_hash, "password123"
    )  # Vérifie que le hash est bien vérifié
    assert user.email == new_user.email  # Vérifie que l'utilisateur est retourné


def test_authenticate_user_wrong_password(mocker, new_user):
    """Test d'échec de connexion avec un mauvais mot de passe"""
    mock_get_user = mocker.patch(
        "backend.dao.auth_dao.UserDAO.get_user_by_email", return_value=new_user
    )
    mock_check_password = mocker.patch(
        "backend.services.auth_service.check_password_hash", return_value=False
    )  # 🔹 Mauvais mot de passe

    #  Récupérer la réponse et le status code
    response, status_code = AuthService.authenticate_user(
        new_user.email, "wrong_password"
    )

    mock_get_user.assert_called_once_with(new_user.email)
    mock_check_password.assert_called_once_with(
        new_user.password_hash, "wrong_password"
    )

    #  Vérifier séparément la réponse et le code HTTP
    assert response == {"error": "Incorrect password"}
    assert status_code == 401


def test_authenticate_non_existent_user(mocker):
    """Test d'échec de connexion avec un utilisateur inexistant"""
    mock_get_user = mocker.patch(
        "backend.dao.auth_dao.UserDAO.get_user_by_email", return_value=None
    )

    response, status_code = AuthService.authenticate_user(
        "unknown@example.com", "password123"
    )

    assert response == {"error": "User not found"}
    assert status_code == 404
