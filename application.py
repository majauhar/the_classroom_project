from app import app, db
from app.models import Teacher, Student, Assignment

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Teacher': Teacher , 'Assignment': Assignment}