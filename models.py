from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db= SQLAlchemy()

def connect_db(app):
    with app.app_context():
        db.app = app
        db.init_app(app)
        db.create_all()

"""Models for Blogly."""

class User(db.Model):

    __tablename__ = "users"

    id= db.Column(db.Integer,
                  primary_key=True,
                  autoincrement=True)
    first_name = db.Column(db.String(50),
                  nullable=False)
    last_name = db.Column(db.String(50),
                  nullable=False)
    image_url= db.Column(db.String,nullable=True)

    user_posts = db.relationship('Post', backref='users', cascade='all, delete-orphan')


    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        u = self
        return f"<User id={u.id}> first_name={u.first_name} last_name={u.last_name} image_url= {u.image_url}"
    
class Post(db.Model):

    __tablename__ = "posts" 

    id = db.Column(db.Integer,
                   primary_key= True,
                   autoincrement=True)
    title = db.Column(db.Text,
                      nullable=False)
    content = db.Column(db.Text,
                      nullable=False)
    created_at = db.Column(db.DateTime,default = datetime.utcnow)

    user_id =db.Column(db.Integer,
                       db.ForeignKey('users.id'),nullable=False)
    
    user = db.relationship('User', backref='posts')

    