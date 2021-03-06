"""empty message

Revision ID: f1caa5bb3b64
Revises: f16a8632ed0d
Create Date: 2017-07-11 15:42:50.086985

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f1caa5bb3b64'
down_revision = 'f16a8632ed0d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('session_id', postgresql.UUID(as_uuid=True), server_default=sa.text(u'uuid_generate_v4()'), nullable=True))
    op.create_unique_constraint(None, 'users', ['session_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'session_id')
    # ### end Alembic commands ###
