"""Add doctor_id relationship to User model

Revision ID: 012
Revises: 011_audit_logs
Create Date: 2026-08-10 13:55:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = '012'
down_revision = '011_audit_logs'
branch_labels = None
depends_on = None


def _has_column(table: str, column: str) -> bool:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    return column in [c["name"] for c in inspector.get_columns(table)]


def upgrade() -> None:
    if not _has_column("users", "doctor_id"):
        with op.batch_alter_table("users") as batch_op:
            batch_op.add_column(sa.Column("doctor_id", sa.Integer(), nullable=True))
            batch_op.create_foreign_key(
                "fk_users_doctor_id",
                "doctors",
                ["doctor_id"],
                ["id"],
                ondelete="SET NULL",
            )
        op.create_index("ix_users_doctor_id", "users", ["doctor_id"])


def downgrade() -> None:
    op.drop_index("ix_users_doctor_id", table_name="users")
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_constraint("fk_users_doctor_id", type_="foreignkey")
        batch_op.drop_column("doctor_id")
