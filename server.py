from flask import Flask, current_app
# redirect
from flask import redirect, url_for
# template
from flask import render_template
# converter
from converters import MyConverter

app = Flask('flask-practice')
app.url_map.converters['re'] = MyConverter

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/center/<re(r"\d{5,10}"):uid>')
def center(uid):
    return f"user: {uid}"

@app.route('/phone/<re(r"09\d{8}"):phone_number>')
def phone(phone_number):
    return f"phone number: {phone_number}"

@app.route('/login')
def login():
    return redirect(url_for('center', uid='12311'))


if __name__ == '__main__':
    app.config.from_pyfile('./config/config.cfg')
    # print(app.url_map.converters)
    app.run(host='0.0.0.0', port=5000)