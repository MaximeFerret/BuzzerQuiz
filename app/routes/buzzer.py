from flask import Blueprint

buzzer = Blueprint("buzzer", __name__)


@buzzer.route("/buzz")
def buzz():
    return "Buzzer Page"
