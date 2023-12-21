from flask_login import UserMixin
from sqlalchemy.orm import mapped_column
from sqlalchemy import DateTime, ForeignKey, Integer, String
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from init import db

class User(UserMixin, db.Model):
    """
    Class that represents a user of the application

    The following attributes of a user are stored in this table:
        * email - email address of the user
        * hashed password - hashed password (using werkzeug.security)
        * registered_on - date & time that the user registered

    REMEMBER: Never store the plaintext password in a database!
    """

    __tablename__ = 'users'
    id = mapped_column(Integer(), primary_key=True, autoincrement=True)
    username = mapped_column(String(), unique=True, nullable=False)
    password_hashed = mapped_column(String(128), nullable=False)
    registered_on = mapped_column(DateTime(), nullable=False)
    
    def __init__(self, username: str, password_plaintext: str):
        """Create a new User object using the email address and hashing the
        plaintext password using Werkzeug.Security.
        """
        self.username = username
        self.password_hashed = self._generate_password_hash(password_plaintext)
        self.registered_on = datetime.now()

    def is_password_correct(self, password_plaintext: str):
        return check_password_hash(self.password_hashed, password_plaintext)

    def set_password(self, password_plaintext: str):
        self.password_hashed = self._generate_password_hash(password_plaintext)

    @staticmethod
    def _generate_password_hash(password_plaintext):
        return generate_password_hash(password_plaintext)


