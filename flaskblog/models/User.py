from flaskblog import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    profile_image = db.Column(
        db.String(50), nullable=False, default='default.jpg')
    bio = db.Column(db.String(120), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    last_login = db.Column(db.DateTime, nullable=True,
                           default=datetime.utcnow)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_at=1800):
        s = Serializer(app.secret_key, expires_at)
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verfiy_reset_token(token):
        s = Serializer(app.secret_key)
        try:
            user_id = s.load(token)
        except:
            return None
        return User.query.get(user_id)

    def toJSON(self):
        return {'username': self.username, 'id': self.id}
    def __repr__(self):
        return self.username
