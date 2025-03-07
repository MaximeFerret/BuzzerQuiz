from backend.business_object.db import db
from backend.business_object.user import User
from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_socketio import SocketIO
#from flask_wtf.csrf import CSRFProtect
from backend.controller.user_ctrl import auth_bp
from backend.controller.quiz_ctrl import quiz_bp
from backend.utils.socketio_events import socketio


app = Flask(__name__, template_folder="frontend/templates")
app.config.from_object("backend.config.Config")
socketio.init_app(app)

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(auth_bp)
app.register_blueprint(quiz_bp, url_prefix="/quiz")


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "authentication.login"

#csrf = CSRFProtect(app)
#socketio = SocketIO(app, cors_allowed_origins="*")

# app.permanent_session_lifetime = app.config['PERMANENT_SESSION_LIFETIME']


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def homepage():
    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        #print("Flask URL Map:", app.url_map)  # 打印所有可用路由

        db.create_all()  # Crée la base de données si elle n'existe pas encore
    socketio.run(app, host="0.0.0.0", debug=True)
