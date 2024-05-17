"""Added offers and payment tables

Revision ID: 1fcdca5b265b
Revises: 522da4c622ba
Create Date: 2024-05-17 20:38:26.039786

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1fcdca5b265b'
down_revision = '522da4c622ba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('offers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('employer_id', sa.Integer(), nullable=False),
    sa.Column('job_seeker_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('accept_status', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['employer_id'], ['employers.id'], name=op.f('fk_offers_employer_id_employers')),
    sa.ForeignKeyConstraint(['job_seeker_id'], ['jobseekers.id'], name=op.f('fk_offers_job_seeker_id_jobseekers')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('jobseeker_id', sa.Integer(), nullable=True),
    sa.Column('employer_id', sa.Integer(), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('payment_date', sa.Date(), nullable=False),
    sa.Column('payment_status', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['employer_id'], ['employers.id'], name=op.f('fk_payments_employer_id_employers')),
    sa.ForeignKeyConstraint(['jobseeker_id'], ['jobseekers.id'], name=op.f('fk_payments_jobseeker_id_jobseekers')),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payments')
    op.drop_table('offers')
    # ### end Alembic commands ###
