from application import db
from application import login
from flask_login import UserMixin 
from datetime import datetime

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=1)
    fullname = db.Column(db.String(100), nullable=0)
    username = db.Column(db.String(100), unique=1 , nullable=0)
    email = db.Column(db.String(100), unique=1 , nullable=0)
    password = db.Column(db.String(100) , nullable=0)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    posts = db.relationship('Post', backref='author', lazy="joined")

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', {self.image_file})"
    
class Post(db.Model):
    id =   db.Column(db.Integer, primary_key=1)
    title = db.Column(db.String(10), nullable=0)
    content = db.Column(db.Text, nullable=0)
    date_posted = db.Column(db.DateTime, nullable=0, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=0)


    def __repr__(self):
        return (f"Post ('{self.title}', '{self.date_posted}, [author: {self.user_id}])")

