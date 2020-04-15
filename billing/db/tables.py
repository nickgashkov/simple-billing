import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

metadata = sa.MetaData()

users = sa.Table(
    'users', metadata,
    sa.Column(
        'id',
        postgresql.UUID(),
        primary_key=True,
        server_default=sa.text("uuid_generate_v4()"),
    ),
    sa.Column('username', sa.String(), unique=True),
    sa.Column('password', sa.String()),
)

wallets = sa.Table(
    'wallets', metadata,
    sa.Column(
        'id',
        postgresql.UUID(),
        primary_key=True,
        server_default=sa.text("uuid_generate_v4()"),
    ),
    sa.Column('user_id', postgresql.UUID(), sa.ForeignKey('users.id')),
)

operations = sa.Table(
    'operations', metadata,
    sa.Column(
        'id',
        postgresql.UUID(),
        primary_key=True,
        server_default=sa.text("uuid_generate_v4()"),
    ),
    sa.Column('wallet_id', sa.ForeignKey('wallets.id')),
)


tables = (
    users,
)
