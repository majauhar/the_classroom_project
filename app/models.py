from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm import relationship, backref

relationship_table=db.Table('relationship_table', 
                             db.Column('user_id', db.Integer,db.ForeignKey('user.id'), nullable=False),
                             db.Column('course_id',db.Integer,db.ForeignKey('course.id'),nullable=False),
                             db.PrimaryKeyConstraint('user_id', 'course_id') )

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    courses = db.relationship('Course', secondary=relationship_table, backref='users')
    submissions = db.relationship('Submission', backref='author', lazy = 'dynamic')

    
    def __repr__(self):
        return '<User {}>'.format(self.username)
    def set_access(self, access = 0):
        self.access = access
    def is_teacher(self):
        return self.access == 1
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(64), index = True)
    code = db.Column(db.String(64), index = True, unique = True)
    assignments = db.relationship('Assignment', backref='course', lazy = 'dynamic')
    instructor = db.Column(db.Integer)

    def __repr__(self):
        return '{} : {}'.format(self.title, self.code).capitalize()


class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    body = db.Column(db.String(300))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    submissions = db.relationship('Submission', backref='problem', lazy = 'dynamic')

    def __repr__(self):
        return '<Problem: {}>'.format(self.body)

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(300))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'))

    def __repr__(self):
        return '<Solution: {}>'.format(self.body)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))