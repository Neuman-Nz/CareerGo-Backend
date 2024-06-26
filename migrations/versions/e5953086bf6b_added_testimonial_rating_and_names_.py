"""Added testimonial, rating and names columns

Revision ID: e5953086bf6b
Revises: 3b9bdf7bfa44
Create Date: 2024-05-14 14:19:29.055512

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5953086bf6b'
down_revision = '3b9bdf7bfa44'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('testimonial', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('app_rating', sa.Integer(), nullable=True))

    with op.batch_alter_table('jobseekers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('first_name', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('last_name', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('linkedin_link', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('testimonial', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('app_rating', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('jobseekers', schema=None) as batch_op:
        batch_op.drop_column('app_rating')
        batch_op.drop_column('testimonial')
        batch_op.drop_column('linkedin_link')
        batch_op.drop_column('last_name')
        batch_op.drop_column('first_name')

    with op.batch_alter_table('employers', schema=None) as batch_op:
        batch_op.drop_column('app_rating')
        batch_op.drop_column('testimonial')

    # ### end Alembic commands ###
