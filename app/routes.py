from flask import render_template
from app import app, db
from app.forms import LoginForm, RegistrationForm, NewCourse, NewAssignment, JoinCourse, SubmitAnswer
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Course, Assignment, Submission


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

@app.route('/joincourse',  methods=['GET', 'POST'])
@login_required
def joincourse():
    form = JoinCourse()
    user = current_user
    if form.validate_on_submit():
        course = Course.query.filter_by(code=form.code.data).first_or_404()
        if course:
            course.users.append(user)
            db.session.commit()
            flash('Class successfully joined!')
        else:
            flash('Invalid Code')
        return redirect(url_for('course'))
    return render_template('joincourse.html', form=form)
        

@app.route('/opencourse/<code>')
@login_required
def opencourse(code):
    user = current_user
    course = Course.query.filter_by(code=code).first_or_404()
    assignments = course.assignments.all()
    # instructor = User.query.filter_by(id=course.instructor).first_or_404()
    students = course.users
    return render_template('course.html', assignments = assignments, students=students, course=course)

@app.route('/deletecourse/<code>')
@login_required
def deletecourse(code):
    user = current_user
    course = Course.query.filter_by(code=code).first_or_404()
    user.courses.remove(course)
    db.session.delete(course)
    db.session.commit()

    flash('This course has been deleted!')
    return redirect(url_for('course'))


# new assignment route
@app.route('/<code>/newassignment',  methods=['GET', 'POST'])
@login_required
def newassignment(code):
    form = NewAssignment()
    user = current_user
    course = Course.query.filter_by(code=code).first_or_404()
    if form.validate_on_submit():
        assignment = Assignment(title=form.title.data, body=form.body.data)
        course.assignments.append(assignment)
        db.session.add(assignment)
        db.session.commit()
        
        flash('Congratulations, you have added a new question!')
        return redirect(url_for('opencourse', code=code))
    return render_template('newassignment.html', title='New Assignment', form=form)


@app.route('/<code>/openassignment/<id>')
@login_required
def openassignment(code, id):
    user = current_user
    course = Course.query.filter_by(code=code).first_or_404()
    assignment = Assignment.query.filter_by(id=id).first_or_404()
    return render_template('assignment.html', assignment = assignment, course=course)
@app.route('/<code>/<id>/deleteassignment/')
@login_required
def deleteassignment(code, id):
    # user = current_user
    assignment = Assignment.query.filter_by(id=id).first_or_404()
    course = Course.query.filter_by(code=code).first_or_404()
    course.assignments.remove(assignment)
    db.session.delete(assignment)
    db.session.commit()

    flash('The assignment has been deleted!')
    return redirect(url_for('opencourse', code=code))

@app.route('/<code>/<id>/submit',   methods=['GET', 'POST'])
@login_required
def submitassignment(code, id):
    user = current_user
    form = SubmitAnswer()
    assignment = Assignment.query.filter_by(id=id).first_or_404()
    if form.validate_on_submit():
        submission = Submission(body=form.body.data, user_id = user.id, assignment_id=id)
        assignment.submissions.append(submission)
        user.submissions.append(submission)
        db.session.add(submission)
        db.session.commit()
        
        flash('Congratulations, you have submitted the solution!')
        return redirect(url_for('opencourse', code=code))
    return render_template('assignmentsubmit.html', title='New submission', form=form)

