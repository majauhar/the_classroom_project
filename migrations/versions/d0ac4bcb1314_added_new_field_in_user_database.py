"""added new field in user database

Revision ID: d0ac4bcb1314
Revises: 2aed7f829e64
Create Date: 2019-11-18 17:13:58.612896

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd0ac4bcb1314'
down_revision = '2aed7f829e64'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('faculty_id', sa.String(length=16), nullable=True))
    op.add_column('user', sa.Column('fullname', sa.String(length=64), nullable=True))
    op.create_index(op.f('ix_user_faculty_id'), 'user', ['faculty_id'], unique=True)
    op.create_index(op.f('ix_user_fullname'), 'user', ['fullname'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_fullname'), table_name='user')
    op.drop_index(op.f('ix_user_faculty_id'), table_name='user')
    op.drop_column('user', 'fullname')
    op.drop_column('user', 'faculty_id')
    # ### end Alembic commands ###
