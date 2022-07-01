"""empty message

Revision ID: 2e3bd0076f9e
Revises: 2d6af6d9d9ef
Create Date: 2022-06-28 15:08:09.632014

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e3bd0076f9e'
down_revision = '2d6af6d9d9ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bank_member',
    sa.Column('image_file', sa.Text(), nullable=False),
    sa.Column('bank_member_id', sa.Integer(), nullable=False),
    sa.Column('bank_member_name', sa.String(), nullable=False),
    sa.Column('bank_member_position', sa.String(), nullable=False),
    sa.Column('bank_member_about', sa.String(length=320), nullable=True),
    sa.Column('bank_member_email_id', sa.String(length=320), nullable=False),
    sa.Column('bank_member_contact', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('bank_member_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bank_member')
    # ### end Alembic commands ###