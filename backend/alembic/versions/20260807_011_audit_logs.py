"""Tabela de auditoria para registrar alterações nas entidades do domínio

Revision ID: 011_audit_logs
Revises: 009_doctor_hour_rate_computed
Create Date: 2026-08-07

Cria a tabela `audit_logs` com os campos especificados em spec 007 / data-model.md.
Esta é a infraestrutura para registrar quem alterou o quê (escala, horas extras, cadastros)
com valor antes/depois, mantendo a trilha viva mesmo após deleção da entidade auditada.

A trilha nasce vazia; não há histórico anterior a recuperar (research R1-R3 da spec).
"""
from alembic import op
import sqlalchemy as sa

revision = "011_audit_logs"
down_revision = "009_doctor_hour_rate_computed"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("user_label", sa.String(255), nullable=False),
        sa.Column("user_role", sa.String(20), nullable=False),
        sa.Column("origin", sa.String(10), nullable=False),
        sa.Column("action", sa.String(10), nullable=False),
        sa.Column("resource", sa.String(30), nullable=False),
        sa.Column("resource_id", sa.Integer(), nullable=True),
        sa.Column("period_id", sa.Integer(), nullable=True),
        sa.Column("before", sa.JSON(), nullable=True),
        sa.Column("after", sa.JSON(), nullable=True),
        sa.Column("summary", sa.String(255), nullable=True),
        sa.Column("correlation_id", sa.String(36), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_audit_logs_user_id", ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index("ix_audit_logs_occurred_at", "audit_logs", ["occurred_at"])
    op.create_index("ix_audit_logs_resource", "audit_logs", ["resource", "resource_id"])
    op.create_index("ix_audit_logs_user_id", "audit_logs", ["user_id"])
    op.create_index("ix_audit_logs_period_id", "audit_logs", ["period_id"])


def downgrade() -> None:
    op.drop_index("ix_audit_logs_period_id", table_name="audit_logs")
    op.drop_index("ix_audit_logs_user_id", table_name="audit_logs")
    op.drop_index("ix_audit_logs_resource", table_name="audit_logs")
    op.drop_index("ix_audit_logs_occurred_at", table_name="audit_logs")
    op.drop_table("audit_logs")
