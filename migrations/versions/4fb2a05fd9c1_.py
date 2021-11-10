"""empty message

Revision ID: 4fb2a05fd9c1
Revises: 
Create Date: 2021-11-07 20:53:23.782428

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4fb2a05fd9c1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Profile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('userID', sa.String(length=64), nullable=False),
    sa.Column('first_name', sa.String(length=64), nullable=False),
    sa.Column('last_name', sa.String(length=64), nullable=False),
    sa.Column('address_id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Profile_address'), 'Profile', ['address'], unique=False)
    op.create_index(op.f('ix_Profile_address_id'), 'Profile', ['address_id'], unique=False)
    op.create_index(op.f('ix_Profile_email'), 'Profile', ['email'], unique=True)
    op.create_index(op.f('ix_Profile_first_name'), 'Profile', ['first_name'], unique=False)
    op.create_index(op.f('ix_Profile_last_name'), 'Profile', ['last_name'], unique=False)
    op.create_index(op.f('ix_Profile_userID'), 'Profile', ['userID'], unique=True)
    op.create_table('address',
    sa.Column('address_id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(length=120), nullable=True),
    sa.Column('city', sa.String(length=120), nullable=True),
    sa.Column('state', sa.String(length=10), nullable=True),
    sa.Column('country', sa.String(length=10), nullable=True),
    sa.Column('zipcode', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('address_id')
    )
    op.create_index(op.f('ix_address_address'), 'address', ['address'], unique=False)
    op.create_index(op.f('ix_address_city'), 'address', ['city'], unique=False)
    op.create_index(op.f('ix_address_country'), 'address', ['country'], unique=False)
    op.create_index(op.f('ix_address_state'), 'address', ['state'], unique=False)
    op.create_index(op.f('ix_address_zipcode'), 'address', ['zipcode'], unique=False)
    op.create_table('flask_dance_oauth',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('token', sa.JSON(), nullable=False),
    sa.Column('provider', sa.String(length=256), nullable=False),
    sa.Column('provider_user_id', sa.String(length=256), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['Profile.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('provider_user_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('flask_dance_oauth')
    op.drop_index(op.f('ix_address_zipcode'), table_name='address')
    op.drop_index(op.f('ix_address_state'), table_name='address')
    op.drop_index(op.f('ix_address_country'), table_name='address')
    op.drop_index(op.f('ix_address_city'), table_name='address')
    op.drop_index(op.f('ix_address_address'), table_name='address')
    op.drop_table('address')
    op.drop_index(op.f('ix_Profile_userID'), table_name='Profile')
    op.drop_index(op.f('ix_Profile_last_name'), table_name='Profile')
    op.drop_index(op.f('ix_Profile_first_name'), table_name='Profile')
    op.drop_index(op.f('ix_Profile_email'), table_name='Profile')
    op.drop_index(op.f('ix_Profile_address_id'), table_name='Profile')
    op.drop_index(op.f('ix_Profile_address'), table_name='Profile')
    op.drop_table('Profile')
    # ### end Alembic commands ###