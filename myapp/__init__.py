from flask import (
    Flask
)

# mysql
from flask_sqlalchemy import SQLAlchemy
import pymysql

mysql = SQLAlchemy()

def create_app(settings=None):
    app = Flask('myapp', static_folder='./static')
    # 引入 settings
    app.config.from_pyfile('./config/config.cfg')
    
    # register blueprint
    import myapp.api.v1
    app.register_blueprint(myapp.api.v1.application, url_prefix='/v1')
    
    return app
    

def create_backend(settings=None):
    app = create_app(settings)
    # register blueprint
    import myapp.backend
    app.register_blueprint(myapp.backend.application, url_prefix='/backend')
    return app