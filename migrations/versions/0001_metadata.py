"""Initial append-only metadata and durable technical job tables."""

import sqlalchemy as sa
from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "documents",
        sa.Column("kind", sa.String(128), primary_key=True),
        sa.Column("id", sa.String(128), primary_key=True),
        sa.Column("version", sa.Integer, primary_key=True),
        sa.Column("body", sa.Text, nullable=False),
        sa.Column("content_hash", sa.String(64), nullable=False),
        sa.Column("created_at", sa.String(40), nullable=False),
    )
    op.create_table(
        "audit",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("actor", sa.String(128), nullable=False),
        sa.Column("action", sa.String(128), nullable=False),
        sa.Column("resource", sa.String(256), nullable=False),
        sa.Column("outcome", sa.String(64), nullable=False),
        sa.Column("details", sa.Text, nullable=False),
        sa.Column("created_at", sa.String(40), nullable=False),
    )
    op.create_table(
        "runs",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("state", sa.String(32), nullable=False),
        sa.Column("config", sa.Text, nullable=False),
        sa.Column("config_hash", sa.String(64), nullable=False),
        sa.Column("manifest", sa.Text, nullable=False),
        sa.Column("manifest_hash", sa.String(64), nullable=False),
        sa.Column("result", sa.Text),
        sa.Column("error", sa.Text),
        sa.Column("owner", sa.String(128)),
        sa.Column("created_by", sa.String(128), nullable=False),
        sa.Column("parent_run_id", sa.String(36), sa.ForeignKey("runs.id")),
        sa.Column("created_at", sa.String(40), nullable=False),
        sa.Column("started_at", sa.String(40)),
        sa.Column("finished_at", sa.String(40)),
    )
    op.create_index("ix_runs_queue", "runs", ["state", "created_at"])
    for table in ("documents", "audit"):
        for operation in ("UPDATE", "DELETE"):
            op.execute(
                f"CREATE TRIGGER {table}_deny_{operation.lower()} BEFORE {operation} ON {table} "
                "BEGIN SELECT RAISE(ABORT, 'Append-only record cannot be modified'); END"
            )
    op.execute(
        "CREATE TRIGGER runs_immutable_inputs BEFORE UPDATE OF "
        "id, config, config_hash, manifest, manifest_hash, created_by, parent_run_id, created_at "
        "ON runs BEGIN SELECT RAISE(ABORT, 'Run inputs cannot be modified'); END"
    )
    op.execute(
        "CREATE TRIGGER runs_deny_delete BEFORE DELETE ON runs "
        "BEGIN SELECT RAISE(ABORT, 'Run history cannot be deleted'); END"
    )


def downgrade() -> None:
    raise RuntimeError("Destructive rollback is disabled. Restore a verified coherent backup.")
