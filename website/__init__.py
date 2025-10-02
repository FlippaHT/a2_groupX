from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Global extensions (do not bind to app yet)
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # --- Config ---
    app.config['SECRET_KEY'] = 'replace_this_with_a_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # --- Init extensions ---
    db.init_app(app)
    login_manager.init_app(app)

    # Where to redirect unauthenticated users
    login_manager.login_view = 'routes.login'
    login_manager.login_message_category = 'info'

    # --- Blueprints ---
    from .routes import routes
    app.register_blueprint(routes)

    # --- User loader for Flask-Login ---
    from .models import User
    @login_manager.user_loader
    def load_user(user_id: str):
        # Flask-Login stores id as str; convert to int for PK
        return User.query.get(int(user_id))

    # Ensure tables exist (safe to call repeatedly)
    with app.app_context():
        db.create_all()

    return app
