"""init database

Revision ID: 001_init
Revises:
Create Date: 2026-06-24
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "001_init"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # doctors
    op.create_table(
        "doctors",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("crm", sa.String(length=20), nullable=False),
        sa.Column("hour_rate", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column(
            "active",
            sa.Boolean(),
            server_default="1",
            nullable=False,
        ),
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
        sa.PrimaryKeyConstraint("id", name="pk_doctors"),
        sa.CheckConstraint("hour_rate >= 0", name="ck_doctor_hour_rate_positive"),
    )
    op.create_index("ix_doctors_crm", "doctors", ["crm"], unique=True)
    op.create_index("ix_doctors_active", "doctors", ["active"])

    # periods
    op.create_table(
        "periods",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("month", sa.Integer(), nullable=False),
        sa.Column(
            "status",
            sa.String(length=20),
            server_default="draft",
            nullable=False,
        ),
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
        sa.PrimaryKeyConstraint("id", name="pk_periods"),
        sa.UniqueConstraint("year", "month", name="uq_period_year_month"),
        sa.CheckConstraint(
            "month BETWEEN 1 AND 12", name="ck_period_month_range"
        ),
        sa.CheckConstraint(
            "year BETWEEN 2000 AND 2100", name="ck_period_year_range"
        ),
    )
    op.create_index("ix_periods_status", "periods", ["status"])

    # shifts
    op.create_table(
        "shifts",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "period_id",
            sa.Integer(),
            sa.ForeignKey("periods.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("shift_date", sa.Date(), nullable=False),
        sa.Column("shift_type", sa.String(length=5), nullable=False),
        sa.Column(
            "status",
            sa.String(length=20),
            server_default="scheduled",
            nullable=False,
        ),
        sa.Column("scheduled_start", sa.DateTime(timezone=True), nullable=True),
        sa.Column("scheduled_end", sa.DateTime(timezone=True), nullable=True),
        sa.Column("actual_start", sa.DateTime(timezone=True), nullable=True),
        sa.Column("actual_end", sa.DateTime(timezone=True), nullable=True),
        sa.Column("total_duration_minutes", sa.Integer(), nullable=True),
        sa.Column("doctor_count", sa.Integer(), nullable=True),
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
        sa.PrimaryKeyConstraint("id", name="pk_shifts"),
        sa.UniqueConstraint(
            "shift_date", "shift_type", name="uq_shift_date_type"
        ),
    )
    op.create_index("ix_shifts_period_id", "shifts", ["period_id"])
    op.create_index("ix_shifts_shift_date", "shifts", ["shift_date"])
    op.create_index(
        "ix_shifts_period_date", "shifts", ["period_id", "shift_date"]
    )

    # shift_parts
    op.create_table(
        "shift_parts",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "shift_id",
            sa.Integer(),
            sa.ForeignKey("shifts.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "doctor_id",
            sa.Integer(),
            sa.ForeignKey("doctors.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("start_time", sa.Time(), nullable=False),
        sa.Column("end_time", sa.Time(), nullable=False),
        sa.Column(
            "status",
            sa.String(length=20),
            server_default="planned",
            nullable=False,
        ),
        sa.Column("duration_minutes", sa.Integer(), nullable=True),
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
        sa.PrimaryKeyConstraint("id", name="pk_shift_parts"),
        sa.CheckConstraint(
            "start_time < end_time", name="ck_shift_part_time_order"
        ),
    )
    op.create_index("ix_shift_parts_shift_id", "shift_parts", ["shift_id"])
    op.create_index("ix_shift_parts_doctor_id", "shift_parts", ["doctor_id"])
    op.create_index(
        "ix_shift_parts_doctor_date",
        "shift_parts",
        ["doctor_id", "shift_id"],
    )

    # shift_extras
    op.create_table(
        "shift_extras",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "shift_id",
            sa.Integer(),
            sa.ForeignKey("shifts.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "doctor_id",
            sa.Integer(),
            sa.ForeignKey("doctors.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("justification", sa.Text(), nullable=False),
        sa.Column(
            "status",
            sa.String(length=20),
            server_default="pending",
            nullable=False,
        ),
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
        sa.PrimaryKeyConstraint("id", name="pk_shift_extras"),
    )
    op.create_index("ix_shift_extras_shift_id", "shift_extras", ["shift_id"])
    op.create_index("ix_shift_extras_doctor_id", "shift_extras", ["doctor_id"])


def downgrade() -> None:
    op.drop_table("shift_extras")
    op.drop_table("shift_parts")
    op.drop_table("shifts")
    op.drop_table("periods")
    op.drop_table("doctors")
