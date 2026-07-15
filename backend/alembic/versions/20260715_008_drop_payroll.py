"""drop payroll — remove superfície payroll/cobertura sem uso (spec 006, B-07)

Revision ID: 008_drop_payroll
Revises: 007_create_users
Create Date: 2026-07-15

A tabela payrolls nunca teve tela consumidora (o pagamento real é o relatório
PDF/Excel gerado a partir da escala; a folha oficial é feita no ERP). As três
tabelas de snapshot (coverage_snapshots, financial_snapshots, financial_facts)
nunca foram criadas por migration — só existem em bancos de dev/test antigos
(via create_all) — por isso o drop delas é condicional, via inspector (mesmo
padrão da migration 004).

ATENÇÃO (deploy): fazer backup antes de aplicar (scripts/backup.sh) — o
downgrade recria o schema de payrolls, mas não os dados.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "008_drop_payroll"
down_revision: Union[str, None] = "007_create_users"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table("payrolls")

    # Tabelas sem migration de criação: dropar apenas se existirem (dev/test antigos)
    inspector = sa.inspect(op.get_bind())
    existing = set(inspector.get_table_names())
    for table in ("financial_facts", "financial_snapshots", "coverage_snapshots"):
        if table in existing:
            op.drop_table(table)


def downgrade() -> None:
    # Recria payrolls com o schema da migration 003 (dados não retornam).
    # As tabelas de snapshot não são recriadas — nunca existiram no schema versionado.
    op.create_table(
        "payrolls",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("period_id", sa.Integer(), nullable=False),
        sa.Column("year_month", sa.String(6), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="draft"),
        sa.Column("current_version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_by", sa.String(100), nullable=False, server_default="system"),
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
        sa.Column("reopen_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("reopen_reason", sa.Text(), nullable=True),
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
