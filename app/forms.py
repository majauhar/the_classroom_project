from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User, Course, Assignment, Submission

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    fullname = StringField('Full Name', validators=[DataRequired()])
    faculty_id = StringField('Faculty ID', validators=[DataRequired()])

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
    def validate_faculty_id(self, faculty_id):
        user = User.query.filter_by(faculty_id=faculty_id.data).first()
        if user is not None:
            raise ValidationError('This faculty ID is already a user!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class NewCourse(FlaskForm):
    title = StringField('Course Title', validators = [DataRequired()])
    code = StringField('Course Code', validators = [DataRequired()])
    submit = SubmitField('Submit')

    def validate_code(self, code):
        code = Course.query.filter_by(code=code.data).first()
        if code is not None:
            raise ValidationError('This course is already running!')
    

# assignment form
class NewAssignment(FlaskForm):
    title = StringField('Assignment Title', validators = [DataRequired()])
    body = StringField('Assignment body', validators = [DataRequired()])
    submit = SubmitField('Submit')

# join course form
class JoinCourse(FlaskForm):
    code = StringField('Course Code', validators = [DataRequired()])
    submit = SubmitField('Submit')
# submission form
class SubmitAnswer(FlaskForm):
    body = StringField('Submission body', validators = [DataRequired()])
    submit = SubmitField('Submit')
