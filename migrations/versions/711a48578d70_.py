"""empty message

Revision ID: 711a48578d70
Revises: 9dd572db74e8
Create Date: 2022-06-11 23:42:21.483067

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '711a48578d70'
down_revision = '9dd572db74e8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('user_first_name', sa.String(length=20), nullable=False))
    op.add_column('user', sa.Column('user_last_name', sa.String(length=20), nullable=False))
    op.drop_column('user', 'last_name')
    op.drop_column('user', 'first_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('first_name', sa.VARCHAR(length=20), autoincrement=False, nullable=False))
    op.add_column('user', sa.Column('last_name', sa.VARCHAR(length=20), autoincrement=False, nullable=False))
    op.drop_column('user', 'user_last_name')
    op.drop_column('user', 'user_first_name')
    # ### end Alembic commands ###
