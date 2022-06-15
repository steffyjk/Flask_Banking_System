"""empty message

Revision ID: f6bebe6d88fb
Revises: 711a48578d70
Create Date: 2022-06-13 14:31:02.121909

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6bebe6d88fb'
down_revision = '711a48578d70'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('u_p', sa.String(length=320), nullable=True))
    op.drop_column('user', 'user_phone_number')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('user_phone_number', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('user', 'u_p')
    # ### end Alembic commands ###