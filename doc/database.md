# Mysql
這邊以 SQLAlchemy 做演示
```bash=
pip install flask-sqlalchemy
pip install pymysql
```

建立連接, 常用設定
```python=
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql

pymysql.install_as_MySQLdb()
mysql = SQLAlchemy()

app = Flask(__name__)

# 設定 mysql url
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@127.0.0.1:3306/db_flask'
# db 與 model 同步修改
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 查詢時顯示 SQL 語句
app.config['SQLALCHEMY_ECHO'] = True

mysql.init_app(app)
```