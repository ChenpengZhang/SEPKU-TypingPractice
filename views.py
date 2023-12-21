#-*-coding:gb2312-*-
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from models import User
from init import db

@login_required
def index():
    return render_template('index.html')

#��¼��ͼ
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
                #�����û�ID
                return redirect(url_for('index'))
            else:
                flash('��¼ʧ�ܣ������û���������')
        else:
            flash('�û�������')
    return render_template('login.html')


#�ǳ���ͼ
#@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

#ע����ͼ
#@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_username = request.form['username']
        new_password = request.form['password']
        
        user = User.query.filter_by(username = new_username).first()
        if user:
            flash('�û����ѱ�ע��')
        else:
            new_user = User(username = new_username, password_plaintext=new_password)
            db.session.add(new_user)
            db.session.commit()
            flash('�û�ע��ɹ�')
            return redirect(url_for('login'))
    return render_template('register.html')

#@app.route('/update_target', methods=['POST'])
def update_target():
    target_text = "Hello World this is typing practice"
    # ��������һЩ����������֤�ı���ʽ��

    # ��Ŀ���ı�ͨ��AJAX��Ӧ���͸���ҳ
    return jsonify({'status': 'success', 'text': target_text})



