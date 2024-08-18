from flask import Flask
from .extension import db, login_manager, bcrypt
from .auth import auth
from .admin import admin
from .user import user
from .general_routes import route
from .searchBluePrint import search
from .updateProfile import profile
from .databaseModel import User


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
    app.config['SECRET_KEY'] = 'any_secret_key'

    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.register_blueprint(user)
    app.register_blueprint(profile)
    app.register_blueprint(search)
    app.register_blueprint(route)

    login_manager.init_app(app)
    bcrypt.init_app(app)
    db.init_app(app)

    with app.app_context():
        import application.databaseModel
        db.create_all()

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

    return app