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
    # Usa o inspector do SQLAlchemy (portável) em vez de PRAGMA (só SQLite),
    # para a migration funcionar tanto em SQLite (dev) quanto em Postgres (prod).
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    return any(col["name"] == column_name for col in inspector.get_columns(table_name))


def upgrade() -> None:
    if not column_exists("doctors", "specialty"):
        op.add_column(
            "doctors",
            sa.Column("specialty", sa.String(100), nullable=False, server_default="Clínica Médica"),
        )


def downgrade() -> None:
    if column_exists("doctors", "specialty"):
        op.drop_column("doctors", "specialty")
