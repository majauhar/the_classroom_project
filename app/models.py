from app import db
from datetime import datetime

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    #-- added a post relationship
    #-- supposed to be related to Courses in future
    posts = db.relationship('Assignment', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<Professor {}>'.format(self.username)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<Student {}>'.format(self.username)

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(300))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))

    def __repr__(self):
        return '<Problem {}>'.format(self.body)