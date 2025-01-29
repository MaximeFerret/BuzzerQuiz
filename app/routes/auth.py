from flask import Blueprint, jsonify, request

from app.models.user import User

auth_routes = Blueprint("auth_routes", __name__)

# Stockage temporaire des utilisateurs (remplacer par une base de données)
users = {}


@auth_routes.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username in users:
        return jsonify({"error": "Username already exists"}), 400

    user = User(username, password)
    users[username] = user
    return jsonify({"message": "User registered", "user_id": user.id}), 201


@auth_routes.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = users.get(username)
    if user and user.password == password:
        return jsonify({"message": "Login successful", "user_id": user.id}), 200

    return jsonify({"error": "Invalid credentials"}), 401
