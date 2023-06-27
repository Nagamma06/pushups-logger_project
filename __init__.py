from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask_login import LoginManager

# create the extension
db = SQLAlchemy()


# override inbuilt method
def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/pushup_logger_db'
    db.init_app(app)


    # Check the database connection
    # try:
    #     with app.app_context():
    #         db.create_all()
    #         print("Database connection successful!")
    # except Exception as e:
    #     print("Error connecting to the database:", str(e))
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    return app
