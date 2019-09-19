from flask import render_template
from app import app


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