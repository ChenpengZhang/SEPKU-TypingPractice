#-*-coding:utf8-*-
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from models import User,Level,UserLevel,get_level_content
from database import db
from models import get_level_content, set_user_level, get_sorted_user_list, get_user_level


@login_required
def index():
    username = session.get('username', None)
    user_id = session.get('user_id', None)
    return render_template('Index.html', user_id=user_id, username=username)

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
                session['user_id'] = user_id
                session['username'] = username
                
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
    user_id = int(request.form['user_id'])
    username = request.form['username']
    level_id = int(request.form['level'])
    completion_time = float(request.form['time'])
    correct_rate = float(request.form['correct_rate'])
    set_user_level(user_id, username, level_id, completion_time, correct_rate)
    
    return jsonify({'status': 'success'})

#@app.route('/vimlevel')
@login_required
def vimlevel():
    user_id = session.get('user_id', None)
    return render_template('vimlevel.html', user_id=user_id)

#@app.route('/rank')
@login_required
def rank():
    return render_template('rank.html')

#@app.route('/get_sorted_Userlist', methods=['POST'])
def get_sorted_Userlist():
    """
    接收关卡ID
    """
    level_id = int(request.form['level'])
    return jsonify({'status': 'success', 'data': get_sorted_user_list(level_id)}) #返回的是一个列表，其中的元素为(完成时间，正确率，用户名)，按照完成时间排序

#根据用户ID和关卡ID返回关卡的练习时间和正确率
def get_practice_record():
    """
    接收用户ID和相应的关卡ID
    """
    user_id = int(request.form['user_id'])
    level_id = int(request.form['level_id'])
    print("here")
    print("user_id: ", user_id)
    
    if level_id != -1:
        return jsonify({'status': 'success', 'data': get_user_level(user_id, level_id)})
    else:
        return jsonify({'status': 'success', 'data': get_user_level(user_id)}) # 一个列表，包含用户已经练习的关卡的记录，元素是（关卡ID、用户完成时间、提交时间、正确率）

#用户个人练习记录
def get_record():
    user_id = session.get('user_id', None)
    return render_template("record.html", user_id = user_id)