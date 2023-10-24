from .. import app

@app.route('/')
def index():
    return 'ok', 200