from flask import Flask, render_template
from routes.quiz import quiz  # Import du Blueprint

app = Flask(__name__)

# Enregistrement du Blueprint
app.register_blueprint(quiz)


@app.route("/")
def home():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)
