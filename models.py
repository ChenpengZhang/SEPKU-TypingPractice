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

    __tablename__ = 'user'
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
    def _generate_password_hash(password_plaintext, method='pbkdf2:sha256', salt_length=8):
        return generate_password_hash(password_plaintext, method=method, salt_length=salt_length)


class Level(db.Model):

    __tablename__ = 'level'

    id = mapped_column(Integer(), primary_key=True, autoincrement=True)
    level_id = mapped_column(Integer(),unique=True,nullable=False)
    title = mapped_column(String(128), nullable=False)
    content = mapped_column(String(),nullable=False)
    difficulty = db.Column(db.Integer) 

    
    def __init__(self, level_id: int, title: str, content: str, difficulty: int):
        
        self.level_id=level_id
        self.title=title
        self.content=content
        self.difficulty=difficulty

    def get_content(self):
        return self.content
    
    def get_level_id(self):
        return self.level_id
    
    def get_title(self):
        return self.title
    
    def get_difficulty(self):
        return self.difficulty
    

    
def set_level_byfile(road:str):   #通过给定路径文件，建立一个关卡
    with open(road, 'r') as file:
        data = file.read().strip()
        parts = data.split('@')

        if len(parts) != 4:
            return 1

        level_id, difficulty, title, content = parts
        level_id = int(level_id)
        difficulty = int(difficulty)

        # 检查 level_id 是否已经存在
        if Level.query.filter_by(level_id=level_id).first() is not None:
            return 2
        
        # 创建 Level 实例
        new_level = Level(level_id=level_id, title=title, content=content, difficulty=difficulty)
        
        # 添加到数据库会话并提交
        db.session.add(new_level)
        db.session.commit()

        return 0


def get_level_content(level_id:int):
    # 根据 level_id 查询 Level 实例
    level = Level.query.filter_by(level_id=level_id).first()
    
    # 检查是否找到了对应的 Level
    if level is not None:
        # 返回找到的 Level 的内容
        return (
            level.get_title(),
            level.get_difficulty(),
            level.get_content())
        
    else:
        # 如果没有找到，返回错误信息
        return None

class UserLevel(db.Model):
    __tablename__ = 'userlevel'
    id = mapped_column(db.Integer, primary_key=True)
    user_id = mapped_column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    level_id = mapped_column(db.Integer, db.ForeignKey('level.id'), nullable=False)
    completion_time = mapped_column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('user_levels', lazy=True))
    level = db.relationship('Level', backref=db.backref('user_levels', lazy=True))

#求出排行榜
def get_sorted_user_list(level_id):
    user_list = UserLevel.query.filter_by(level_id=level_id).order_by(UserLevel.completion_time).all()
    sorted_list = [( entry.completion_time,entry.user_id) for entry in user_list]
    return sorted_list