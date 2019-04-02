from flaskblog import db
from datetime import datetime

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    # slug = db.Column(db.String(50), unique=True, nullable=False)
    image = db.Column(db.String(50), nullable=True, default='default.jpg')
    content = db.Column(db.String(100*100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    likes = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"{self.title}, {self.content}, {self.created_at}"
