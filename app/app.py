from flask import Flask
from app.models import db, User
from flask_login import LoginManager
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'safety-helmet-secret-key-12345'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    with app.app_context():
        db.create_all()

    return app
