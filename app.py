#-*-coding:gb2312-*-
from init import create_app
from views import index, login, logout, register, update_target

app = create_app()
app.add_url_rule('/', 'index', index)
app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
app.add_url_rule('/logout', 'logout', logout)
app.add_url_rule('/register', 'register', register, methods=['GET', 'POST'])
app.add_url_rule('/update_target', 'update_target', update_target, methods=['POST'])
app.run(debug=True)