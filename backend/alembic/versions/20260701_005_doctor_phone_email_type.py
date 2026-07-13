"""Add doctor phone, email, doctor_type fields

Revision ID: 005
Revises: 004_doctor_specialty_active
Create Date: 2026-07-01
"""
from alembic import op
import sqlalchemy as sa

revision = "005"
down_revision = "004_doctor_specialty_active"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("doctors", sa.Column("phone", sa.String(20), nullable=True))
    op.add_column("doctors", sa.Column("email", sa.String(255), nullable=True))
    op.add_column(
        "doctors",
        sa.Column("doctor_type", sa.String(30), nullable=False, server_default="plantonista"),
    )


def downgrade() -> None:
    op.drop_column("doctors", "doctor_type")
    op.drop_column("doctors", "email")
    op.drop_column("doctors", "phone")
