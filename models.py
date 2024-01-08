from xml.sax import ContentHandler
from flask_login import UserMixin
from sqlalchemy.orm import mapped_column
from sqlalchemy import DateTime, ForeignKey, Integer, String
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from database import db

# 用户数据表
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


# 关卡数据表
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
    with open(road, 'r', encoding='utf-8', errors='ignore') as file:
        data = file.read().strip()
        parts = data.split('@')

        if len(parts) != 4:
            return 1

        level_id, difficulty, title, content = parts
        level_id = int(level_id)
        difficulty = int(difficulty)

        # 检查 level_id 是否已经存在
        level = Level.query.filter_by(level_id=level_id).first()
        if level is not None:
            level.level_id = level_id
            level.title = title
            level.content = content
            level.difficulty = difficulty
            db.session.commit()
            return 0
        
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

# 用户练习记录数据表
class UserLevel(db.Model):
    __tablename__ = 'userlevel'

    id = mapped_column(Integer(), primary_key=True, autoincrement = True)
    user_id = mapped_column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    level_id = mapped_column(db.Integer, db.ForeignKey('level.id'), nullable=False)
    completion_time = mapped_column(db.Float)  #这个是完成打字所花的时间，单位为秒，需要后端记录一下
    handin_time = mapped_column(db.DateTime, default=datetime.utcnow)  #这个是提交的时间戳
    correct_rate = mapped_column(db.Float)
    user = db.relationship('User', backref=db.backref('user_levels', lazy=True))
    level = db.relationship('Level', backref=db.backref('user_levels', lazy=True))


    def __init__(self, user_id , level_id , completion_time, handin_time, correct_rate):
        self.user_id = user_id
        self.level_id = level_id
        self.completion_time = completion_time
        self.handin_time = handin_time
        self.correct_rate = correct_rate

    def get_user_level(self):
        return (self.user_id, self.level_id)
    
    def get_completion_time(self):
        return self.completion_time
    
    def get_handin_time(self):
        return self.handin_time
    
    def get_correct_rate(self):
        return self.correct_rate
    
#根据用户ID和level ID写入某个用户某篇level的练习时间和正确率
def set_user_level(user_id, level_id, completion_time, correct_rate):
    user_level = UserLevel.query.filter_by(user_id=user_id, level_id=level_id).first()
    if user_level is None:
        new_user_level = UserLevel(user_id=user_id, level_id=level_id, completion_time=completion_time, handin_time=datetime.utcnow(), correct_rate=correct_rate)
        db.session.add(new_user_level)
    else:
        user_level.completion_time = completion_time
        user_level.handin_time = datetime.utcnow()
        user_level.correct_rate = correct_rate
    db.session.commit()
    return 0

#根据用户ID和level ID读取练习时间和正确率，若未给定level ID，则返回该用户所有level的练习时间和正确率
def get_user_level(user_id, level_id=None):
    if level_id is None:
        user_levels = UserLevel.query.filter_by(user_id=user_id).all()
        return [(user_level.level_id, user_level.completion_time, user_level.handin_time, user_level.correct_rate) for user_level in user_levels]
    else:
        user_level = UserLevel.query.filter_by(user_id=user_id, level_id=level_id).first()
        if user_level is None:
            return -1
        else:
            return (user_level.level_id, user_level.completion_time, user_level.handin_time, user_level.correct_rate)

#求出排行榜
def get_sorted_user_list(level_id):
    user_list = UserLevel.query.filter_by(level_id=level_id).order_by(UserLevel.completion_time).all()
    sorted_list = [( entry.completion_time,entry.user_id) for entry in user_list]
    return sorted_list

#求出前十名
def get_top_ten(level_id):
    user_list = UserLevel.query.filter_by(level_id=level_id).order_by(UserLevel.completion_time).limit(10).all()
    top_ten = [(entry.user_id, entry.completion_time) for entry in user_list]
    return top_ten

