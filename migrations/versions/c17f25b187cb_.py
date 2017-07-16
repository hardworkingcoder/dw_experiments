"""empty message

Revision ID: c17f25b187cb
Revises: f77e7019708c
Create Date: 2017-07-11 15:14:12.435600

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c17f25b187cb'
down_revision = 'f77e7019708c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('nickname', sa.String(), nullable=True))
    op.add_column('users', sa.Column('social_id', sa.String(), nullable=True))
    op.drop_constraint(u'users_ddw_user_id_key', 'users', type_='unique')
    op.create_unique_constraint(None, 'users', ['social_id'])
    op.drop_column('users', 'ddw_user_id')
    op.drop_column('users', 'ddw_display_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('ddw_display_name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('ddw_user_id', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'users', type_='unique')
    op.create_unique_constraint(u'users_ddw_user_id_key', 'users', ['ddw_user_id'])
    op.drop_column('users', 'social_id')
    op.drop_column('users', 'nickname')
    # ### end Alembic commands ###
