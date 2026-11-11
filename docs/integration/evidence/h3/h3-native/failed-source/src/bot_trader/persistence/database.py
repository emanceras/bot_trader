"""SQLite connection lifecycle. Application startup never creates schema implicitly."""

from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from sqlite3 import Connection as SQLiteConnection

from alembic import command
from alembic.config import Config
from sqlalchemy import Connection, create_engine, event, inspect, text
from sqlalchemy.pool import ConnectionPoolEntry

from bot_trader.core.errors import Conflict
from bot_trader.core.settings import Settings

SCHEMA_REVISION = "0001"


def _configure_connection(connection: SQLiteConnection, _: ConnectionPoolEntry) -> None:
    cursor = connection.cursor()
    try:
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA busy_timeout=10000")
    finally:
        cursor.close()


class Database:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.path = settings.database_path
        self.engine = create_engine(
            f"sqlite:///{self.path}", connect_args={"check_same_thread": False, "timeout": 10}
        )
        event.listen(self.engine, "connect", _configure_connection)

    @contextmanager
    def transaction(self) -> Iterator[Connection]:
        """Serialize metadata mutations on a single SQLite host, including claims."""
        with self.engine.connect() as connection:
            connection.exec_driver_sql("BEGIN IMMEDIATE")
            try:
                yield connection
                connection.commit()
            except BaseException:
                connection.rollback()
                raise

    def close(self) -> None:
        self.engine.dispose()


def migrate(database: Database) -> None:
    """Explicit operator action; never called by Repository or HTTP startup."""
    database.path.parent.mkdir(parents=True, exist_ok=True)
    root = database.settings.repository_root.resolve()
    script = root / "migrations"
    if not (script / "env.py").is_file():
        raise Conflict("Migration files are missing from the configured repository root.")
    config = Config(str(root / "alembic.ini"))
    config.set_main_option("script_location", str(script))
    with database.engine.begin() as connection:
        config.attributes["connection"] = connection
        command.upgrade(config, "head")
    check_schema(database)


def check_schema(database: Database) -> None:
    if not Path(database.path).is_file():
        raise Conflict("Metadata database is missing; run the explicit migration command.")
    with database.engine.connect() as connection:
        names = set(inspect(connection).get_table_names())
        if not {"alembic_version", "documents", "audit", "runs"}.issubset(names):
            raise Conflict("Metadata schema is missing or incomplete; migrate explicitly.")
        version: object = connection.execute(
            text("SELECT version_num FROM alembic_version")
        ).scalar_one()
        if version != SCHEMA_REVISION:
            raise Conflict("Metadata schema version is incompatible.")
