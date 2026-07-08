"""create users table

Revision ID: 007_create_users
Revises: 006
Create Date: 2026-07-08
"""
from alembic import op
import sqlalchemy as sa

revision = "007_create_users"
down_revision = "006"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("role", sa.String(20), nullable=False, server_default="CONSULTA"),
        sa.Column("active", sa.Boolean(), nullable=False, server_default="1"),
        sa.Column("last_login", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint(
            "role IN ('ADMIN','COORDENADOR','FINANCEIRO','MEDICO','CONSULTA')",
            name="ck_users_role_valid",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_active", "users", ["active"])


def downgrade() -> None:
    op.drop_table("users")
