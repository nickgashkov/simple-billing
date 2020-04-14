import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

metadata = sa.MetaData()

users = sa.Table(
    'users', metadata,
    sa.Column('id', postgresql.UUID(), primary_key=True),
    sa.Column('username', sa.String()),
    sa.Column('password', sa.String()),
)
