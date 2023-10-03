from flask import Flask, current_app

app = Flask('flask-practice')

@app.route('/')
def hello_world():
    print(current_app.config)
    return 'hello world'

if __name__ == '__main__':
    app.config.from_pyfile('./config/config.cfg')
    app.run(host='0.0.0.0', port=5000)