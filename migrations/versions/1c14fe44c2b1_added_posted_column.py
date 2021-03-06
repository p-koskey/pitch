"""Added posted column

Revision ID: 1c14fe44c2b1
Revises: a88a243c6a8d
Create Date: 2020-09-23 20:58:03.423823

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1c14fe44c2b1'
down_revision = 'a88a243c6a8d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pitches', sa.Column('posted', sa.DateTime(), nullable=True))
    op.drop_column('pitches', 'pitched')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pitches', sa.Column('pitched', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('pitches', 'posted')
    # ### end Alembic commands ###
