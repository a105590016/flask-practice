from flask import Flask, current_app, abort
# request, response
from flask import request, make_response, jsonify
# redirect
from flask import redirect, url_for
# template
from flask import render_template
# session
from flask import session
from flask_session import Session
# mysql
from flask_sqlalchemy import SQLAlchemy
import pymysql
# 從資料夾取得文件
from flask import send_from_directory

# wtf 表單
from flask_wtf import FlaskForm
# 表單欄位
from wtforms import SubmitField, StringField, PasswordField
# 表單驗證
from wtforms.validators import DataRequired, EqualTo

from werkzeug.utils import secure_filename
# converter
from converters import MyConverter

import os, redis
from datetime import datetime


# 初始化 session
f_session = Session()
f_mysql = SQLAlchemy()

app = Flask('flask-practice')
app.url_map.converters['re'] = MyConverter

class HeroType(f_mysql.Model):
    __tablename__ = 'hero_types'
    
    id = f_mysql.Column(f_mysql.Integer, primary_key=True)
    name = f_mysql.Column(f_mysql.String(32), unique=True)
    
    # 關聯, db 不會存在此欄位, 僅用來查詢與反向查詢
    # backref: 在關連的另一個 model 加入反向引用
    heros = f_mysql.relationship("Hero", backref="type")
    
    
class Hero(f_mysql.Model):
    __tablename__ = 'heros'
    id = f_mysql.Column(f_mysql.Integer, primary_key=True)
    name = f_mysql.Column(f_mysql.String(64), unique=True)
    gender = f_mysql.Column(f_mysql.String(64))
    
    # fk, one hero_type map many heros
    type_id = f_mysql.Column(f_mysql.Integer, f_mysql.ForeignKey('hero_types.id'))
    


# 自定義 502 錯誤訊息
@app.errorhandler(502)
def handle_502_error(error):
    print(error)
    return 'server error'


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
    if uid == '123456':
        # 提前中斷程式, 並回傳錯誤訊息
        abort(502)
        
    return f"user: {uid}"

@app.route('/phone/<re(r"09\d{8}"):phone_number>')
def phone(phone_number):
    return f"phone number: {phone_number}"
    return redirect(url_for('center_page', uid='12311'))

@app.route('/session/create', methods=['GET', 'POST'])
def session_create():
    session['uid'] = '123456'
    session['username'] = 'evan123456'
    return redirect('/user')

@app.route('/session/delete')
def session_delete():
    # 刪除 session 的三種方式
    session.pop('uid')
    del session['username']
    session.clear()
    return redirect('/user')

@app.route('/user')
def user():
    username = session.get('username')
    
    if username:
        return f"user: {username}"
    
    return 'please login first'

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
    
    
@app.route('/define_response')
def define_response():
    # (response, status_code, headers)
    # return ('test 自定義 responese', 444, {"name": "evan", "value": 1234 })

    # 可不加括號, 會自動轉成 set
    # return 'test 自定義 responese', 444, {"name": "evan", "value": 1234 }

    # 自定義 status code, 可加上描述訊息
    # return 'test 自定義 responese', '444 error1234', {"name": "evan", "value": 1234 }
    
    resp = make_response('123')
    resp.headers['name'] = 'evan'
    resp.status_code = '444 error12345'
    return resp


@app.route('/json_response')
def json_response():
    data = {
        'name': 'evan',
        'value': 1234
    }
    return jsonify(data)


@app.route('/doc')
def doc():
    return send_from_directory('doc', 'session.md')

@app.route('/doc/<path:path>')
def send_doc(path):
    return send_from_directory('doc', path)

@app.route('/init/mysql')
def init_mysql_data():
    f_mysql.drop_all()
    f_mysql.create_all()
    
    # 添加一筆
    type1 = HeroType(name='射手')
    f_mysql.session.add(type1)
    f_mysql.session.commit()
    
    # 添加多筆
    type2 = HeroType(name='坦克')
    type3 = HeroType(name='法師')
    type4 = HeroType(name='刺客')
    f_mysql.session.add_all([type2, type3, type4])
    f_mysql.session.commit()
    
    hero1 = Hero(name='后羿', gender='男', type_id=type1.id)
    hero2 = Hero(name='程咬金', gender='男', type_id=type2.id)
    hero3 = Hero(name='王昭君', gender='女', type_id=type3.id)
    hero4 = Hero(name='安琪拉', gender='女', type_id=type3.id)
    hero5 = Hero(name='蘭陵王', gender='男', type_id=type4.id)
    f_mysql.session.add_all([hero1, hero2, hero3, hero4, hero5])
    f_mysql.session.commit()
    

@app.route('/hero/<int:hero_id>')
def hero(hero_id):
    hero = Hero.query.filter_by(id=hero_id).first_or_404()
    data = {
        'id': hero.id,
        'name': hero.name,
        'gender': hero.gender,
        'type': hero.type.name
    }
    return jsonify(data)

@app.route('/type/<int:type_id>/heros')
def get_heros_by_type(type_id):
    hero_type = HeroType.query.filter_by(id=type_id).first_or_404()
    data = {
        'name': hero_type.name,
        'heros': [ {'id': hero.id, 'name': hero.name} for hero in hero_type.heros ]
    }
    return jsonify(data)

@app.route('/hero/<int:hero_id>/update')
def update_hero(hero_id):
    # update 1
    # hero = Hero.query.get(hero_id)
    # hero.name = '伽羅'
    # f_mysql.session.add(hero)
    # f_mysql.session.commit()
    
    # update 2
    Hero.query.filter_by(id=hero_id).update({'name': '虞姬', 'gender': '女'})
    f_mysql.session.commit()
    return 'ok'

@app.route('/hero/<int:hero_id>/delete')
def delete_hero(hero_id):
    hero = Hero.query.get(hero_id)
    f_mysql.session.delete(hero)
    f_mysql.session.commit()
    return 'ok'

@app.route('/template/<filename>')
def get_template(filename):
    return render_template(f"{filename}.html")


# 自定義表單, 文字, 密碼, 提交按鈕
class LoginForm(FlaskForm):
    account = StringField(label='帳號: ', validators=[DataRequired('帳號不能為空')])
    password = PasswordField(label='密碼: ', validators=[DataRequired('密碼不能為空'), EqualTo('password1', '密碼不一樣')])
    password1 = PasswordField(label='確認密碼', validators=[DataRequired('請再次輸入密碼')])
    submit = SubmitField('提交')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        account = form.account.data
        password = form.password.data
        password1 = form.password1.data
        print(account, password, password1)
        
    return render_template('login.html', form=form)
    
    
if __name__ == '__main__':
    # 引入 settings
    app.config.from_pyfile('./config/config.cfg')
    app.jinja_env.filters['handletime'] = handletime  # 注册过滤器
    app.jinja_env.filters['handletime_with_param'] = handletime_with_param  # 注册过滤器
    # print(app.url_map.converters)
    
    # 綁定 app
    # session
    app.config['SESSION_REDIS'] = redis.Redis(host=app.config['SESSION_REDIS_HOST'], port=app.config['SESSION_REDIS_PORT'], db=app.config['SESSION_REDIS_DB'])
    f_session.init_app(app)
    # mysql
    pymysql.install_as_MySQLdb()
    f_mysql.init_app(app)
    
    app.run(host='0.0.0.0', port=5000)