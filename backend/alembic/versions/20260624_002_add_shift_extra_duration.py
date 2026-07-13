"""add duration_minutes to shift_extras

Revision ID: 002_add_shift_extra_duration
Revises: 001_init
Create Date: 2026-06-24
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "002_add_shift_extra_duration"
down_revision: Union[str, None] = "001_init"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "shift_extras",
        sa.Column(
            "duration_minutes",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )


def downgrade() -> None:
    op.drop_column("shift_extras", "duration_minutes")
