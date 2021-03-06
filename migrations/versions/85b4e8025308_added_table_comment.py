"""added table Comment

Revision ID: 85b4e8025308
Revises: ecd2368e1c15
Create Date: 2020-09-22 15:35:24.484951

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '85b4e8025308'
down_revision = 'ecd2368e1c15'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('comments', 'pitch_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('comments', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('comments', 'date_posted')
    op.add_column('pitches', sa.Column('downvotes', sa.Integer(), nullable=True))
    op.add_column('pitches', sa.Column('upvotes', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('pitches', 'upvotes')
    op.drop_column('pitches', 'downvotes')
    op.add_column('comments', sa.Column('date_posted', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False))
    op.alter_column('comments', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('comments', 'pitch_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
