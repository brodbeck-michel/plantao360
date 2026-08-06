"""doctor hour_rate vira valor computado (has_rqe + career_start_date)

Revision ID: 009_doctor_hour_rate_computed
Revises: 008_drop_payroll
Create Date: 2026-08-06

O valor da hora do medico deixa de ser digitado manualmente e passa a ser
calculado a partir de duas informacoes cadastrais: se possui RQE e a data de
inicio de carreira, usando a tabela oficial de faixas (M-1..M-5 sem RQE,
E-1..E-5 com RQE). A coluna hour_rate e removida; o valor passa a ser
calculado em runtime (Doctor.hour_rate como property no backend).

ATENCAO: medicos ja cadastrados ficam com career_start_date=NULL ate serem
editados — ate la, o valor calculado cai na faixa base (M-1, R$ 141,00). O
downgrade recria a coluna hour_rate com um valor default, mas nao recupera os
valores antigos (perda de dado conhecida, mesmo padrao da migration 008).
"""
from alembic import op
import sqlalchemy as sa

revision = "009_doctor_hour_rate_computed"
down_revision = "008_drop_payroll"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "doctors",
        sa.Column("has_rqe", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column("doctors", sa.Column("career_start_date", sa.Date(), nullable=True))

    # SQLite não suporta DROP CONSTRAINT/DROP COLUMN direto — batch_alter_table
    # recria a tabela sem a constraint e sem a coluna (mesmo padrão da 003).
    with op.batch_alter_table("doctors", schema=None) as batch_op:
        batch_op.drop_constraint("ck_doctor_hour_rate_positive", type_="check")

    with op.batch_alter_table("doctors", schema=None) as batch_op:
        batch_op.drop_column("hour_rate")


def downgrade() -> None:
    with op.batch_alter_table("doctors", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("hour_rate", sa.Numeric(10, 2), nullable=False, server_default="150.00")
        )

    with op.batch_alter_table("doctors", schema=None) as batch_op:
        batch_op.create_check_constraint("ck_doctor_hour_rate_positive", "hour_rate >= 0")

    op.drop_column("doctors", "career_start_date")
    op.drop_column("doctors", "has_rqe")
