"""Migrations receive a connection from the explicit application migration command."""

from alembic import context
from sqlalchemy import Connection

from bot_trader.persistence.schema import metadata

connection = context.config.attributes.get("connection")
if not isinstance(connection, Connection):
    raise RuntimeError("Use the application's explicit migration command.")
context.configure(connection=connection, target_metadata=metadata)
with context.begin_transaction():
    context.run_migrations()
