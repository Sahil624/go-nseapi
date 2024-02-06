"""empty message

Revision ID: e75f80a7719a
Revises: 
Create Date: 2024-08-06 00:58:02.730328

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e75f80a7719a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.Column('password', sa.LargeBinary(length=128), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('first_name', sa.String(length=30), nullable=True),
    sa.Column('last_name', sa.String(length=30), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('backtest',
    sa.Column('strategy', sa.String(length=50), nullable=False),
    sa.Column('symbol', sa.String(length=20), nullable=False),
    sa.Column('from_date', sa.String(length=10), nullable=False),
    sa.Column('to_date', sa.String(length=10), nullable=False),
    sa.Column('user_id', sa.String(length=36), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('analysis',
    sa.Column('backtest_id', sa.String(length=36), nullable=False),
    sa.Column('result', sa.Text(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['backtest_id'], ['backtest.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('backtest_iterations',
    sa.Column('backtest_id', sa.String(length=36), nullable=False),
    sa.Column('symbol', sa.String(length=20), nullable=True),
    sa.Column('entry_date', sa.Date(), nullable=True),
    sa.Column('entry_price', sa.Float(), nullable=True),
    sa.Column('exit_date', sa.Date(), nullable=True),
    sa.Column('exit_price', sa.Float(), nullable=True),
    sa.Column('size', sa.Integer(), nullable=True),
    sa.Column('direction', sa.String(), nullable=True),
    sa.Column('profit', sa.Float(), nullable=True),
    sa.Column('commission', sa.Float(), nullable=True),
    sa.Column('duration', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['backtest_id'], ['backtest.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('backtest_iterations')
    op.drop_table('analysis')
    op.drop_table('roles')
    op.drop_table('backtest')
    op.drop_table('users')
    # ### end Alembic commands ###
