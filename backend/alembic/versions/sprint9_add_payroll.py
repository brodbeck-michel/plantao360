"""Add payrolls table.

Revision ID: sprint9_payroll
Revises: 002_add_shift_extra_duration
Create Date: 2026-06-26

NOTE (documented 2026-06-28, Sprint 14.3 ETAPA 2):
This migration created the payrolls table with created_at_ts and updated_at_ts
columns that do not exist in the ORM Payroll model. The migration is preserved
as-is to maintain historical immutability. The structural correction is handled
by 003_runtime_alignment, which drops and recreates the table with the correct
schema (DateTime(timezone=True), no duplicate columns).
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "sprint9_payroll"
down_revision: Union[str, None] = "002_add_shift_extra_duration"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
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


def downgrade() -> None:
    op.drop_table("payrolls")
