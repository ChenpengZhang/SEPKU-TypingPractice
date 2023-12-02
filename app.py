from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update_target', methods=['POST'])
def update_target():
    target_text = "Hello World!"
    # 在这里做一些处理，例如验证文本格式等

    # 将目标文本通过AJAX响应发送给网页
    return jsonify({'status': 'success', 'text': target_text})

if __name__ == '__main__':
    app.run()