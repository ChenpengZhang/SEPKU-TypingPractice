from platform import python_revision
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import random
import string
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

#创建数据库
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///typing_practice.db'  # 使用 SQLite 数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@localhost/typing_practice'
db = SQLAlchemy(app)


#配置登录视图
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# 生成随机单词（不符合字典）
def generate_words(min_count, max_count):
    word_count = random.randint(min_count, max_count)

    words = []
    for _ in range(word_count):
        word_length = random.randint(3, 7)  # 假设每个单词长度在 3 到 7 之间
        word = ''.join(random.choices(string.ascii_lowercase, k=word_length))
        words.append(word)

    # 将单词用空格连接成字符串
    return ' '.join(words)

# 定义 User 模型
class User(UserMixin, db.Model):
    #目前只包含ID，用户名和密码。之后可以再加上与练习记录相关的一些字段
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

#加载用户
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

#登录视图
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            user_id = user.id if user else None
            login_user(user)
            #传入用户ID
            return redirect(url_for('index'))
        else:
            flash('登录失败，请检查用户名和密码。')
    return render_template('login.html')

#登出视图
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

#注册视图
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_username = request.form['username']
        new_password = request.form['password']
        
        print(new_username)
        user = User.query.filter_by(username = new_username).first()
        if user:
            flash('用户名已被注册')
        else:
            new_user = User(username = new_username, password = new_password)
            db.session.add(new_user)
            db.session.commit()
            flash('用户注册成功')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/update_target', methods=['POST'])
def update_target():
    target_text = "Hello World this is typing practice"
    # 在这里做一些处理，例如验证文本格式等

    # 将目标文本通过AJAX响应发送给网页
    return jsonify({'status': 'success', 'text': target_text})

if __name__ == '__main__':
    engine = SQLAlchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    inspector = SQLAlchemy.inspect(engine)
    if not inspector.has_table("User"):
        with app.app_context():
            db.drop_all()
            db.create_all()
            app.logger.info('Initialized the database!')
    else:
        app.logger.info('Database already contains the users table.')
        
    print("Python version: ", sys.version)
    app.run()