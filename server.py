from flask import Flask, current_app, request, make_response
# redirect
from flask import redirect, url_for
# template
from flask import render_template
# 從資料夾取得文件
from flask import send_from_directory
from werkzeug.utils import secure_filename
# converter
from converters import MyConverter

import os
from datetime import datetime

app = Flask('flask-practice')
app.url_map.converters['re'] = MyConverter

@app.route('/')
def index():
    ctx = {
        "name": '老王',
        "age": 12,
        "hobby": ["下棋", '电影'],
        "test": {"a": 1, "b": 2},
        "time": datetime.utcnow()
    }
    return render_template('index.html', **ctx)
    # return render_template('index.html', name='laowang', age=12, hobby=["下棋", '电影'], test={"a": 1, "b": 2})  # 加载并渲染模板

@app.route('/center/<re(r"\d{5,10}"):uid>')
def center_page(uid):
    return f"user: {uid}"

@app.route('/phone/<re(r"09\d{8}"):phone_number>')
def phone(phone_number):
    return f"phone number: {phone_number}"

@app.route('/login')
def login():
    return redirect(url_for('center_page', uid='12311'))

# 自定义过滤器
def handletime(time):
   return time.strftime('%Y-%m-%d %H:%M:%S')

# 自定义有參數过滤器
def handletime_with_param(time, mode):
    return time.strftime(mode)

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/center/add', methods=['GET', 'POST'])
def center_add():
    if request.method == 'GET':
        name = request.args.get('name')
        age = request.args.get('age')
        hobby = request.args.getlist('hobby')
        return f"名字: {name} 年齡: {age} 愛好: {hobby}"
    elif request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        hobby = request.form.getlist('hobby')
        return f"名字: {name} 年齡: {age} 愛好: {hobby}"

@app.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
    
    if request.method == 'GET':
        return render_template('upload_image.html')
    else:
        file = request.files.get('file')
        
        if file is None:
            return redirect(request.url)
        
        if file.filename == '':
            return redirect(request.url)
        
        if file and file.filename.split('.')[1] in ALLOWED_EXTENSIONS:
            # 檢查檔案名稱, 並排除中文
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_IMAGE_FOLDER'], filename))
            return redirect(url_for('show', filename=filename))
        
        return "123"
    
@app.route('/show/<filename>')
def show(filename):
    return send_from_directory(app.config['UPLOAD_IMAGE_FOLDER'], filename)

@app.route('/cookie/set', methods=['GET', 'POST'])
def set_cookie():
    resp = make_response(render_template('cookie.html'))
    # set cookie expire time
    # max_age > 10 seconds
    # expires = datetime.utcnow() + timedelta(seconds=10)
    resp.set_cookie('username', 'evan', max_age=1000)
    return resp

@app.route('/cookie/get', methods=['GET', 'POST'])
def get_cookie():
    username = request.cookies.get('username')
    return f"username: {username}"

@app.route('/cookie/delete', methods=['GET', 'POST'])
def delete_cookie():
    resp = make_response('刪除cookie')
    resp.delete_cookie('username')
    return resp
    

if __name__ == '__main__':
    app.config.from_pyfile('./config/config.cfg')
    app.jinja_env.filters['handletime'] = handletime  # 注册过滤器
    app.jinja_env.filters['handletime_with_param'] = handletime_with_param  # 注册过滤器
    # print(app.url_map.converters)
    app.run(host='0.0.0.0', port=5000)