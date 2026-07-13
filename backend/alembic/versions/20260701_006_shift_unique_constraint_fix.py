"""Fix shifts unique constraint to include period_id

Revision ID: 006
Revises: 005
Create Date: 2026-07-01
"""
from alembic import op
import sqlalchemy as sa

revision = "006"
down_revision = "005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("shifts") as batch_op:
        batch_op.drop_constraint("uq_shift_date_type", type_="unique")
        batch_op.create_unique_constraint(
            "uq_shift_period_date_type",
            ["period_id", "shift_date", "shift_type"],
        )


def downgrade() -> None:
    with op.batch_alter_table("shifts") as batch_op:
        batch_op.drop_constraint("uq_shift_period_date_type", type_="unique")
        batch_op.create_unique_constraint(
            "uq_shift_date_type",
            ["shift_date", "shift_type"],
        )
