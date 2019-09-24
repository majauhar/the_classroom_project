from flask import render_template
from app import app
from app.forms import LoginForm
from flask import render_template, flash, redirect, url_for


@app.route('/')
def home():
    return render_template('app_home.html', title='ClassRoom | Welcome')
@app.route('/index')
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
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Log In', form=form)