#-*-coding:utf8-*-
from init import create_app
from views import get_sorted_Userlist, index, login, logout, register, update_target, update_UserLevel, vimlevel, rank, get_practice_record

app = create_app()
app.add_url_rule('/', 'index', index)
app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
app.add_url_rule('/logout', 'logout', logout)
app.add_url_rule('/register', 'register', register, methods=['GET', 'POST'])
app.add_url_rule('/update_target', 'update_target', update_target, methods=['POST'])
app.add_url_rule('/update_UserLevel', 'update_UserLevel', update_UserLevel, methods=['POST'])
app.add_url_rule('/vimlevel', 'vimlevel', vimlevel)
app.add_url_rule('/rank', 'rank', rank)
app.add_url_rule('/get_sorted_Userlist', '/get_sorted_Userlist', get_sorted_Userlist)
app.add_url_rule('/get_practice_record', '/get_practice_record', get_practice_record)
app.run(host='0.0.0.0', port=5000, debug=True)  
# 用gunicorn运行的时候不要写这一行