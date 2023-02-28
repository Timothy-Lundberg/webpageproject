from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5


class User(UserMixin, db.Model):
    """Sätter SQL-kolumner för hur vi ska spara våra användare i databasen"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        """Här hashas lösenordet"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Kollar om hashet i databasen stämmer överens med inskrivna lösenordet"""
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=monsterid&s={}'.format(digest, size)


class Post(db.Model):
    """Sätter SQL-kolumner för hur vi ska spara användarens inlägg i databasen"""

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    page = db.Column(db.Integer)

    def __repr__(self):
        return "Post {}".format(self.body)

    def get_id(self):
        return self.user_id
@login.user_loader
def load_user(user_id):
    """Hittar användaren från databasen"""
    return db.get_or_404(User, int(user_id))
