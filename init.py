from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from flask import Flask
import sqlalchemy as sa


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "login"


def create_app():
    # Create the Flask application
    app = Flask(__name__)

    if os.getenv('DATABASE_URL'):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://", 1)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///typing_practice.db'  # 使用 SQLite 数据库
        
    app.config['SECRET_KEY'] = 'your_secret_key' 
    
    initialize_extensions(app)

    # Check if the database needs to be initialized
    engine = sa.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    inspector = sa.inspect(engine)
    if not inspector.has_table("users"):
        with app.app_context():
            db.drop_all()
            db.create_all()
            app.logger.info('Initialized the database!')
    else:
        app.logger.info('Database already contains the users table.')

    return app




def initialize_extensions(app):
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)
    db.init_app(app)
    login_manager.init_app(app)

    # Flask-Login configuration
    from models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == int(user_id)).first()

