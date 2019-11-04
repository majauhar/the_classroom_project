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
    # courses = relationship('Course', secondary='members')
    courses = db.relationship('Course', secondary=relationship_table, backref='users')
    
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
    
    # def follow(self, course):
    #     if not self.is_following(course):
    #         self.courses.append(course)

    # def unfollow(self, course):
    #     if self.is_following(course):
    #         self.courses.remove(course)

    # def is_following(self, course):
    #     return self.courses.filter(
    #         member.c.followed_id == user.id).count() > 0

class Course(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(64), index = True)
    code = db.Column(db.String(64), index = True, unique = True)
    # users = relationship('User', secondary='members')
    assignments = db.relationship('Assignment', backref='course', lazy = 'dynamic')
    # users = db.relationship('User', secondary=relationship_table, backref='courses' )
    instructor = db.Column(db.Integer)

    def __repr__(self):
        return '{} : {}'.format(self.title, self.code)


# class Member(db.Model):
#     __tablename__ = 'members'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
#     db.UniqueConstraint('user_id', 'course_id', name='UC_user_course')

#     user = relationship(User, backref=backref('members', cascade="all, delete-orphan"))
#     course = relationship(Course, backref=backref('members', cascade="all, delete-orphan"))

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(300))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

    def __repr__(self):
        return '<Problem: {}>'.format(self.body)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))