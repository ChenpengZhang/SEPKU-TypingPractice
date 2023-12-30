#-*-coding:utf8-*-
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from models import User,Level,UserLevel,get_level_content
from database import db
from models import get_level_content, set_user_level


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
            # my_test= Level(1000,"a","b",1)
            # db.session.add(my_test)
            # db.session.commit()
            # outstr=str(get_level_content(1000))

            flash("注册成功")
            return redirect(url_for('login'))
    return render_template('register.html')

#@app.route('/update_target', methods=['POST'])
def update_target():
    """
    接收这个POST方法的表单格式为
    'level': (String)levelnumber
    """
    #text_map = ["Hello World this is typing practice", "Someone knocked at her door just as Victoria was about to leave her flat. It was strange because she hadn't heard the lift or anyone on the stairs. She quickly tried to put on her other shoe and nearly fell over. There were many unopened letters – probably asking for money – on the floor.", "What if this is a banana"]
    # 这里是一个试验，这里的textmap应当是一个关卡对应的语句表
    level = int(request.form['level'])  # 解析需要哪一关
    level -= 1
    target_level_id, target_difficulty, target_text = get_level_content(level)
    return jsonify({'status': 'success', 'text': target_text})  # 返回关卡文本


# 更新用户的练习记录（相应关卡的练习时间和正确率）
#@app.route('/update_UserLevel', methods=['POST'])
def update_UserLevel():
    """
    接收用户ID、关卡ID、练习时间和正确率
    """
    user_id = int(request.form[''])
    level_id = int(request.form[''])
    completion_time = float(request.form[''])
    correct_rate = float(request.form[''])
    set_user_level(user_id, level_id, completion_time, correct_rate)
    
    return
