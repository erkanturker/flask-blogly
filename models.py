from flask_sqlalchemy import SQLAlchemy

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

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        u = self
        return f"<User id={u.id}> first_name={u.first_name} last_name={u.last_name} image_url= {u.image_url}"
    

    
    
    