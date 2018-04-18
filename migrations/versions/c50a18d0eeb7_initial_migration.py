"""initial migration

Revision ID: c50a18d0eeb7
Revises: 
Create Date: 2018-04-18 06:42:44.165533

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c50a18d0eeb7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('name', sa.String(length=64), nullable=True))
    op.create_index(op.f('ix_users_name'), 'users', ['name'], unique=True)
    op.drop_index('ix_users_username', table_name='users')
    op.drop_column('users', 'username')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('username', sa.VARCHAR(length=64), autoincrement=False, nullable=True))
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
    op.drop_index(op.f('ix_users_name'), table_name='users')
    op.drop_column('users', 'name')
    # ### end Alembic commands ###