from sqlalchemy.sql import text
from flask_login import LoginManager
import os
from flask import Flask
from flask.logging import default_handler
from logging.handlers import RotatingFileHandler
import logging
from sqlalchemy import MetaData
from models import set_level_byfile
from database import db
from models import User,Level,UserLevel

#db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "login"

# path to the level file
level_path = "./static/level"

# the column name of each table
column_names = {"user":["id", "username", "password_hashed", "registered_on", "test"], 
               "level":["id", "level_id", "title", "content", "difficulty"], 
               "userlevel":["id", "user_id", "username", "level_id", "completion_time", "handin_time", "correct_rate"]}

def check_columns():
    for column_name in column_names["user"]:
        exists = column_name in User.__table__.columns.keys()
        if not exists:
            return False
    for column_name in column_names["level"]:
        exists = column_name in Level.__table__.columns.keys()
        if not exists:
            return False
    for column_name in column_names["userlevel"]:
        exists = column_name in UserLevel.__table__.columns.keys()
        if not exists:
            return False
    return True

def create_app():
    
    # Create the Flask application
    app = Flask(__name__)

    if os.getenv('DATABASE_URL'):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://", 1)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///typing_practice.db'
        
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
        exists = check_table_exists('user') and check_table_exists('level') and check_table_exists('userlevel')
        if not exists:
            db.drop_all()
            db.create_all()
            app.logger.info('Initialized the database!')
            print('Table does not exist! Initialized the database!')
            #exists = check_table_exists('user') and check_table_exists('level')
            #print("user and level exists? ", exists)
        else:
            if(check_columns()):
                app.logger.info('Database already contains required tables and columns.')
                print("Database already contains required tables and columns.")
            else:
                db.drop_all()
                db.create_all()
                app.logger.info('Initialized the database!')
                print('Missing column! Initialized the database!')
           

        # exists = check_table_exists('level')
        # print("exists: ", exists)
        # if not exists:
        #     db.create_all(tables=[Level.__table__])
        #     app.logger.info('Initialized the database!')
        #     print('Initialized the database!')
        #     exists = check_table_exists('Level')
        #     print("user exists? ", exists)
        # else:
        #     app.logger.info('Database already contains the level table.')

        # check if the level exists and initialize if not
        print("Initializing the levels")
        for filename in os.listdir(level_path):
            filename = os.path.join(level_path, filename)
            error_num = set_level_byfile(filename)
            if(error_num == 1):
                print("Error: check the format of ", filename)
    
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


def check_table_exists(db_name):
    metadata = MetaData()
    metadata.reflect(bind=db.engine)
    return db_name in metadata.tables