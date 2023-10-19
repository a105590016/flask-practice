from server import f_mysql as db

class HeroType(db.Model):
    __tablename__ = 'hero_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    
    # 關聯, db 不會存在此欄位, 僅用來查詢與反向查詢
    # backref: 在關連的另一個 model 加入反向引用
    heros = db.relationship("Hero", backref="type")
    
    
class Hero(db.Model):
    __tablename__ = 'heros'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    gender = db.Column(db.String(64))
    
    # fk, one hero_type map many heros
    type_id = db.Column(db.Integer, db.ForeignKey('hero_types.id'))