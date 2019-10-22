"""new db created

Revision ID: cbee473cb85d
Revises: 
Create Date: 2019-10-19 12:15:27.594071

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cbee473cb85d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('course',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('code', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_course_code'), 'course', ['code'], unique=True)
    op.create_index(op.f('ix_course_title'), 'course', ['title'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('assignment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=300), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_assignment_timestamp'), 'assignment', ['timestamp'], unique=False)
    op.create_table('members',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('members')
    op.drop_index(op.f('ix_assignment_timestamp'), table_name='assignment')
    op.drop_table('assignment')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_course_title'), table_name='course')
    op.drop_index(op.f('ix_course_code'), table_name='course')
    op.drop_table('course')
    # ### end Alembic commands ###