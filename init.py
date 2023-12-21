from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from flask import Flask
import sqlalchemy as sa
from flask.logging import default_handler
from logging.handlers import RotatingFileHandler
import logging
from sqlalchemy import MetaData

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
    #engine = sa.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    #inspector = sa.inspect(engine)
    """
    if not inspector.has_table("users"):
        print("db has no users")
        with app.app_context():
            db.drop_all()
            db.create_all()
            app.logger.info('Initialized the database!')
    """
    with app.app_context():
        exists = check_user_table_exists()
        print("exists: ", exists)
        if not exists:
            db.drop_all()
            db.create_all()
            app.logger.info('Initialized the database!')
            print('Initialized the database!')
            exists = check_user_table_exists()
            print("user exists? ", exists)
        else:
            app.logger.info('Database already contains the user table.')

    
    
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


def configure_logging(app):
    # Logging Configuration
    if app.config['LOG_WITH_GUNICORN']:
        gunicorn_error_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers.extend(gunicorn_error_logger.handlers)
        app.logger.setLevel(logging.DEBUG)
    else:
        file_handler = RotatingFileHandler('instance/flask-user-management.log',
                                           maxBytes=16384,
                                           backupCount=20)
        file_formatter = logging.Formatter('%(asctime)s %(levelname)s %(threadName)s-%(thread)d: %(message)s [in %(filename)s:%(lineno)d]')
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

    # Remove the default logger configured by Flask
    app.logger.removeHandler(default_handler)

    app.logger.info('Starting the Flask User Management App...')


def check_user_table_exists():
    metadata = MetaData()
    metadata.reflect(bind=db.engine)
    return 'user' in metadata.tables