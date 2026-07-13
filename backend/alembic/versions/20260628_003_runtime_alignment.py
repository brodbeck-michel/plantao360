"""runtime alignment — align migrations with ORM models

Revision ID: 003_runtime_alignment
Revises: sprint9_payroll
Create Date: 2026-06-28

Estratégia A: Migration incremental que alinha migrations com modelos ORM.
- Remove CheckConstraint start_time < end_time de shift_parts (não suporta overnight)
- Adiciona CheckConstraint duration_minutes > 0 a shift_parts
- Corrige tabela payrolls (remove colunas duplicadas created_at_ts/updated_at_ts)
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "003_runtime_alignment"
down_revision: Union[str, None] = "sprint9_payroll"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── shift_parts: fix constraints ─────────────────────────────
    # SQLite doesn't support DROP CONSTRAINT, so we use batch_alter_table
    # to recreate the table without the old constraint.
    with op.batch_alter_table("shift_parts", schema=None) as batch_op:
        batch_op.drop_constraint("ck_shift_part_time_order", type_="check")

    with op.batch_alter_table("shift_parts", schema=None) as batch_op:
        batch_op.create_check_constraint(
            "ck_shift_part_duration_positive",
            "duration_minutes > 0",
        )

    # ── payrolls: recreate without duplicate columns ─────────────
    # sprint9_payroll created the table with created_at_ts/updated_at_ts
    # columns that don't exist in the ORM model. We drop and recreate
    # with correct schema (DateTime(timezone=True), no duplicates).
    # This migration is idempotent: it always drops and recreates.
    op.drop_table("payrolls")

    op.create_table(
        "payrolls",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("period_id", sa.Integer(), nullable=False),
        sa.Column("year_month", sa.String(6), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="draft"),
        sa.Column("current_version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_by", sa.String(100), nullable=False, server_default="system"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("reopen_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("reopen_reason", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["period_id"], ["periods.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_payrolls_period_id", "payrolls", ["period_id"])
    op.create_index("ix_payrolls_year_month", "payrolls", ["year_month"])
    op.create_index("ix_payrolls_status", "payrolls", ["status"])
    op.create_index("ix_payrolls_version", "payrolls", ["current_version"])
    op.create_index(
        "ix_payrolls_period_version", "payrolls", ["period_id", "current_version"]
    )


def downgrade() -> None:
    # Reverse: drop corrected payrolls and restore sprint9_payroll schema
    op.drop_table("payrolls")

    # Restore original sprint9_payroll schema (with created_at_ts/updated_at_ts)
    op.create_table(
        "payrolls",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("period_id", sa.Integer(), nullable=False),
        sa.Column("year_month", sa.String(6), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="draft"),
        sa.Column("current_version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_by", sa.String(100), nullable=False, server_default="system"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("reopen_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("reopen_reason", sa.Text(), nullable=True),
        sa.Column("created_at_ts", sa.DateTime(), nullable=True),
        sa.Column("updated_at_ts", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["period_id"], ["periods.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_payrolls_period_id", "payrolls", ["period_id"])
    op.create_index("ix_payrolls_year_month", "payrolls", ["year_month"])
    op.create_index("ix_payrolls_status", "payrolls", ["status"])
    op.create_index("ix_payrolls_version", "payrolls", ["current_version"])
    op.create_index(
        "ix_payrolls_period_version", "payrolls", ["period_id", "current_version"]
    )

    # Restore shift_parts constraints
    with op.batch_alter_table("shift_parts", schema=None) as batch_op:
        batch_op.drop_constraint(
            "ck_shift_part_duration_positive", type_="check"
        )

    with op.batch_alter_table("shift_parts", schema=None) as batch_op:
        batch_op.create_check_constraint(
            "ck_shift_part_time_order",
            "start_time < end_time",
        )
