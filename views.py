#-*-coding:gb2312-*-
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from models import User
from init import db

@login_required
def index():
    return render_template('index.html')

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
                #传入用户ID
                return redirect(url_for('index'))
            else:
                flash('登录失败，请检查用户名和密码')
        else:
            flash('用户不存在')
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
            flash('用户名已被注册')
        else:
            new_user = User(username = new_username, password_plaintext=new_password)
            db.session.add(new_user)
            db.session.commit()
            flash('用户注册成功')
            return redirect(url_for('login'))
    return render_template('register.html')

#@app.route('/update_target', methods=['POST'])
def update_target():
    target_text = "Hello World this is typing practice"
    # 在这里做一些处理，例如验证文本格式等

    # 将目标文本通过AJAX响应发送给网页
    return jsonify({'status': 'success', 'text': target_text})



