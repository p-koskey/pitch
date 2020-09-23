"""Added  like table

Revision ID: a88a243c6a8d
Revises: b9dce9ff18af
Create Date: 2020-09-23 20:54:45.224927

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a88a243c6a8d'
down_revision = 'b9dce9ff18af'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pitch_like',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('pitch_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['pitch_id'], ['pitches.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('pitches', sa.Column('pitched', sa.DateTime(), nullable=True))
    op.drop_column('pitches', 'downvotes')
    op.drop_column('pitches', 'upvotes')
    op.drop_column('pitches', 'posted')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pitches', sa.Column('posted', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('pitches', sa.Column('upvotes', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('pitches', sa.Column('downvotes', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('pitches', 'pitched')
    op.drop_table('pitch_like')
    # ### end Alembic commands ###
