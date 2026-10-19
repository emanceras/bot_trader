"""SQLAlchemy table bindings; only Alembic may create or modify the schema."""

from sqlalchemy import Column, ForeignKey, Integer, MetaData, String, Table, Text

metadata = MetaData()
documents = Table(
    "documents",
    metadata,
    Column("kind", String(128), primary_key=True),
    Column("id", String(128), primary_key=True),
    Column("version", Integer, primary_key=True),
    Column("body", Text, nullable=False),
    Column("content_hash", String(64), nullable=False),
    Column("created_at", String(40), nullable=False),
)
audit = Table(
    "audit",
    metadata,
    Column("id", String(36), primary_key=True),
    Column("actor", String(128), nullable=False),
    Column("action", String(128), nullable=False),
    Column("resource", String(256), nullable=False),
    Column("outcome", String(64), nullable=False),
    Column("details", Text, nullable=False),
    Column("created_at", String(40), nullable=False),
)
runs = Table(
    "runs",
    metadata,
    Column("id", String(36), primary_key=True),
    Column("state", String(32), nullable=False),
    Column("config", Text, nullable=False),
    Column("config_hash", String(64), nullable=False),
    Column("manifest", Text, nullable=False),
    Column("manifest_hash", String(64), nullable=False),
    Column("result", Text),
    Column("error", Text),
    Column("owner", String(128)),
    Column("created_by", String(128), nullable=False),
    Column("parent_run_id", String(36), ForeignKey("runs.id")),
    Column("created_at", String(40), nullable=False),
    Column("started_at", String(40)),
    Column("finished_at", String(40)),
)
