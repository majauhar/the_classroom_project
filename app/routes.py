from flask import render_template
from app import app, db
from app.forms import LoginForm, RegistrationForm, NewCourse
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Course, Assignment


@app.route('/')
def home():
    return render_template('app_home.html', title='ClassRoom | Welcome')
@app.route('/index')
@login_required
def index():
    student = {'username': 'Miguel'}
    assignments = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', student=student, assignments=assignments)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('course'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/course')
@login_required
def course():
    courses = current_user.courses
    user = current_user
    return render_template('courses.html', title='Courses', courses=courses, user=user)

@app.route('/newcourse',  methods=['GET', 'POST'])
@login_required
def newcourse():
    form = NewCourse()
    user = current_user
    if form.validate_on_submit():
        course = Course(title=form.title.data, code=form.code.data, instructor=user.id)
        user.courses.append(course)
        db.session.add(course)
        db.session.commit()
        
        flash('Congratulations, you have created a new course!')
        return redirect(url_for('course'))
    return render_template('newcourse.html', title='New Course', form=form)

@app.route('/opencourse/<code>')
@login_required
def opencourse(code):
    # user = current_user
    course = Course.query.filter_by(code=code).first_or_404()
    assignments = course.assignments.all()
    # instructor = User.query.filter_by(id=course.instructor).first_or_404()
    return render_template('course.html', assignments = assignments)