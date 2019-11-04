from app import app, db
from app.models import User, Course, Assignment, relationship_table

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User':User, 'Course':Course, 'Assignment':Assignment, 'relationship_table':relationship_table}