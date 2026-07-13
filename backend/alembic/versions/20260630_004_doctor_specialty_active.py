"""add doctor specialty field

Revision ID: 004_doctor_specialty_active
Revises: 003_runtime_alignment
Create Date: 2026-06-30

Adiciona campo specialty ao modelo Doctor.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "004_doctor_specialty_active"
down_revision: Union[str, None] = "003_runtime_alignment"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def column_exists(table_name: str, column_name: str) -> bool:
    bind = op.get_bind()
    result = bind.execute(
        sa.text(f"PRAGMA table_info({table_name})")
    )
    return any(row[1] == column_name for row in result)


def upgrade() -> None:
    if not column_exists("doctors", "specialty"):
        op.add_column(
            "doctors",
            sa.Column("specialty", sa.String(100), nullable=False, server_default="Clínica Médica"),
        )


def downgrade() -> None:
    if column_exists("doctors", "specialty"):
        op.drop_column("doctors", "specialty")
