from flask import Blueprint
from flask_login import current_user
from flask_socketio import SocketIO

buzzer_bp = Blueprint("buzzer", __name__)
socketio = SocketIO()

first_buzz = None  # Stocke le premier joueur qui buzz


@socketio.on("buzz")
def handle_buzz(data):
    global first_buzz

    if first_buzz is None:
        first_buzz = (
            current_user.username if current_user.is_authenticated else "Joueur inconnu"
        )

    socketio.emit("buzz_result", {"winner": first_buzz})


@socketio.on("reset_buzzer")
def reset_buzzer():
    global first_buzz
    first_buzz = None
    socketio.emit("buzzer_reset")
