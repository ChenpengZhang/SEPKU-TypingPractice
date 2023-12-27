#-*-coding:utf8-*-
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from models import User
from init import db


@login_required
def index():
    return render_template('Index.html')

#登录视图
#@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            if user.is_password_correct(password):
                user_id = user.id if user else None
                login_user(user)
                
                return redirect(url_for('index'))
            else:
                flash("请检查用户名和密码")
        else:
            flash("用户不存在")
    return render_template('login.html')


#登出视图
#@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

#注册视图
#@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_username = request.form['username']
        new_password = request.form['password']
        
        user = User.query.filter_by(username = new_username).first()
        if user:
            flash("用户名已存在")
        else:
            new_user = User(username = new_username, password_plaintext=new_password)
            db.session.add(new_user)
            db.session.commit()
            flash("注册成功")
            return redirect(url_for('login'))
    return render_template('register.html')

#@app.route('/update_target', methods=['POST'])
def update_target():
    """
    接收这个POST方法的表单格式为
    'level': (String)levelnumber
    """
    text_map = ["Hello World this is typing practice", "Someone knocked at her door just as Victoria was about to leave her flat. It was strange because she hadn't heard the lift or anyone on the stairs. She quickly tried to put on her other shoe and nearly fell over. There were many unopened letters – probably asking for money – on the floor.", "What if this is a banana"]
    # 这里是一个试验，这里的textmap应当是一个关卡对应的语句表
    level = int(request.form['level'])  # 解析需要哪一关
    target_text = text_map[level - 1]
    return jsonify({'status': 'success', 'text': target_text})  # 返回关卡文本



