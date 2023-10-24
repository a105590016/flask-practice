from myapp import mysql as db

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
    
    
class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), unique=True)
    
    # 一對一, 僅關聯, 無實際欄位, 一對一需要把 uselist 設為 False
    content = db.relationship("ArticleContent", backref="article", uselist=False)
    # 一對多
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    
    
class ArticleContent(db.Model):
    __tablename__ = 'article_contents'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text(4000))
    # 一對一, 對應到 articles
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    articles = db.relationship("Article", backref="category")
    
class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
   
# 多對多輔助表
article_tags = db.Table('article_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
    db.Column('article_id', db.Integer, db.ForeignKey('articles.id'))
)

# 自關聯
class Area(db.Model):
    __tablename__ = "areas"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey("areas.id"))

    parent = db.relationship("Area", remote_side=[id])  # 自關聯需要加remote_side