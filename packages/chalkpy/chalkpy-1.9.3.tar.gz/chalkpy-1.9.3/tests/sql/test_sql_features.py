import pytest

from chalk import realtime
from chalk.features import DataFrame, feature, features
from chalk.sql import TempSQLiteFileSource
from chalk.testing import assert_frame_equal

sqlite = TempSQLiteFileSource()

seed_db = """
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS friends;

CREATE TABLE users (
    id TEXT,
    name TEXT
);

CREATE TABLE friends_with (
    u_from TEXT,
    u_to TEXT
);

INSERT INTO users VALUES ('0', 'Wendy'), ('1', 'Shelby');
"""


@pytest.fixture(scope="module")
def init_db():
    session = sqlite.raw_session()
    for statement in seed_db.split(";"):
        if statement != "":
            session.execute(statement)

    session.commit()


@features
class SQLUserFeatures:
    id: str
    name: str


@realtime
def resolve_sql_users_with_fields() -> DataFrame[SQLUserFeatures.id, SQLUserFeatures.name]:
    return sqlite.query_string(
        """
        SELECT id, name FROM users;
        """,
        fields={"id": SQLUserFeatures.id, "name": SQLUserFeatures.name},
    ).all()


@realtime
def resolve_sql_users_without_fields() -> DataFrame[SQLUserFeatures.id, SQLUserFeatures.name]:
    return sqlite.query_string(
        """
        SELECT id, name FROM users;
        """
    ).all()


@realtime
def resolve_sql_users_without_fields_all() -> DataFrame[SQLUserFeatures]:
    return sqlite.query_string(
        """
        SELECT id, name FROM users;
        """
    ).all()


def test_sql_resolver_callable(init_db):
    users = resolve_sql_users_with_fields()
    assert_frame_equal(users, DataFrame({SQLUserFeatures.id: ["0", "1"], SQLUserFeatures.name: ["Wendy", "Shelby"]}))


def test_sql_resolver_no_fields_callable(init_db):
    users = resolve_sql_users_without_fields()
    assert_frame_equal(
        users,
        DataFrame({SQLUserFeatures.id: ["0", "1"], SQLUserFeatures.name: ["Wendy", "Shelby"]}),
    )


def test_sql_resolver_no_fields_all_callable(init_db):
    users = resolve_sql_users_without_fields_all()
    assert_frame_equal(
        users,
        DataFrame({SQLUserFeatures.id: ["0", "1"], SQLUserFeatures.name: ["Wendy", "Shelby"]}),
    )
