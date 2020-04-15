import factory
from factory import fuzzy
from factory.alchemy import SQLAlchemyModelFactory
from pytest_factoryboy import register
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from billing import settings
from billing.auth.authentication import hash_password
from billing.db.tables import operations, users, wallets

ENGINE = create_engine(settings.DB_DSN_TEST)
BASE = declarative_base()
SESSION = scoped_session(
    sessionmaker(
        bind=ENGINE,
        autocommit=True,
        autoflush=True,
    ),
)


# SEE: https://github.com/python/mypy/issues/4300 -- `mypy` does not support
# dynamically created types, so, everything inherited from `BASE` should be
# ignored.
class UserModel(BASE):  # type: ignore
    __table__ = users


class WalletModel(BASE):  # type: ignore
    __table__ = wallets


class OperationModel(BASE):  # type: ignore
    __table__ = operations


class UserFactory(SQLAlchemyModelFactory):
    username = factory.Faker('word')
    password = factory.LazyAttribute(lambda o: hash_password(o.password_raw))
    password_raw = factory.Faker('word')

    class Meta:
        model = UserModel
        sqlalchemy_session = SESSION
        sqlalchemy_session_persistence = 'flush'
        exclude = ('password_raw',)


class WalletFactory(SQLAlchemyModelFactory):
    user_id = factory.LazyAttribute(lambda o: o.user.id)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = WalletModel
        sqlalchemy_session = SESSION
        sqlalchemy_session_persistence = 'flush'
        exclude = ('user',)


class OperationFactory(SQLAlchemyModelFactory):
    wallet_id = factory.LazyAttribute(lambda o: o.wallet.id)
    destination_wallet_id = factory.LazyAttribute(
        lambda o: o.destination_wallet.id
    )
    type = fuzzy.FuzzyChoice(['transfer'])
    amount = factory.Faker('pydecimal')
    timestamp = factory.Faker('date_time')

    wallet = factory.SubFactory(WalletFactory)
    destination_wallet = factory.SubFactory(WalletFactory)

    class Meta:
        model = OperationModel
        sqlalchemy_session = SESSION
        sqlalchemy_session_persistence = 'flush'
        exclude = ('user', 'wallet', 'destination_wallet')


register(UserFactory)
register(WalletFactory)
register(OperationFactory)
