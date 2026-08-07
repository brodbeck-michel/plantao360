"""Testes unitários do AuditService."""

import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.database.base import Base
from app.models.user import User
from app.models.audit_log import AuditLog
from app.services.audit_service import AuditService


@pytest.fixture
def in_memory_db() -> Session:
    """Cria um banco SQLite em memória com schema."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()


@pytest.fixture
def admin_user(in_memory_db: Session) -> User:
    """Cria um usuário admin para testes."""
    user = User(
        id=1,
        name="Admin User",
        email="admin@test.local",
        password_hash="hashed",
        role="ADMIN",
        active=True,
    )
    in_memory_db.add(user)
    in_memory_db.commit()
    return user


class TestAuditServiceRecord:
    """Testes da gravação de auditoria (as 3 ações)."""

    def test_record_create_action(self, in_memory_db: Session, admin_user: User):
        """Testa gravação de ação CREATE."""
        service = AuditService(in_memory_db)

        after = {"doctor_id": 123, "start_time": "08:00", "status": "PLANNED"}
        audit_log = service.record(
            action="create",
            resource="assignment",
            user=admin_user,
            resource_id=1,
            before=None,
            after=after,
            period_id=1,
            summary="Adicionou João Silva ao T1 de 12/08",
        )

        # Invariante 2: create => before is None, after is filled
        assert audit_log.action == "create"
        assert audit_log.before is None
        assert audit_log.after is not None
        assert audit_log.user_id == admin_user.id
        assert audit_log.origin == "user"
        assert audit_log.user_label == admin_user.email
        assert audit_log.user_role == admin_user.role

    def test_record_update_action(self, in_memory_db: Session, admin_user: User):
        """Testa gravação de ação UPDATE."""
        service = AuditService(in_memory_db)

        before = {"start_time": "08:00", "status": "PLANNED"}
        after = {"start_time": "09:00", "status": "CONFIRMED"}
        audit_log = service.record(
            action="update",
            resource="assignment",
            user=admin_user,
            resource_id=1,
            before=before,
            after=after,
            period_id=1,
            summary="Alterou horário de João Silva",
        )

        # Invariante 4: update => ambos preenchidos
        assert audit_log.action == "update"
        assert audit_log.before is not None
        assert audit_log.after is not None
        assert audit_log.resource_id == 1

    def test_record_delete_action(self, in_memory_db: Session, admin_user: User):
        """Testa gravação de ação DELETE."""
        service = AuditService(in_memory_db)

        before = {"doctor_id": 123, "start_time": "08:00", "status": "PLANNED"}
        audit_log = service.record(
            action="delete",
            resource="assignment",
            user=admin_user,
            resource_id=1,
            before=before,
            after=None,
            period_id=1,
            summary="Removeu João Silva do T1",
        )

        # Invariante 3: delete => before filled, after is None
        # Invariante 2 do spec: rastro preservado após deleção (SC-002)
        assert audit_log.action == "delete"
        assert audit_log.before is not None
        assert audit_log.after is None
        assert audit_log.resource_id == 1

    def test_record_filters_fields_for_resource(self, in_memory_db: Session, admin_user: User):
        """Testa que campos sensíveis (FR-004) são filtrados do before/after."""
        service = AuditService(in_memory_db)

        # Tenta gravar com password_hash na lista de campos
        # Isso NÃO deve aparecer no registro (é removido pelo filter_fields)
        after_with_password = {
            "name": "New User",
            "email": "new@test.local",
            "role": "MEDICO",
            "password_hash": "should_not_appear_EVER",  # sensível
            "active": True,
        }
        audit_log = service.record(
            action="create",
            resource="user",
            user=admin_user,
            resource_id=2,
            after=after_with_password,
        )

        # password_hash NÃO deve estar no after gravado
        assert audit_log.after is not None
        assert "password_hash" not in audit_log.after
        assert audit_log.after["name"] == "New User"
        assert audit_log.after["email"] == "new@test.local"

    def test_record_system_origin(self, in_memory_db: Session):
        """Testa gravação com origem='system' (sem usuário)."""
        service = AuditService(in_memory_db)

        audit_log = service.record(
            action="create",
            resource="assignment",
            user=None,  # Sem usuário autenticado
            resource_id=1,
            after={"doctor_id": 100, "status": "PLANNED"},
        )

        # Invariante 5: origin=system => user_id is None, user_role='SYSTEM'
        assert audit_log.origin == "system"
        assert audit_log.user_id is None
        assert audit_log.user_role == "SYSTEM"
        assert audit_log.user_label == "system"

    def test_record_persists_in_session(self, in_memory_db: Session, admin_user: User):
        """Testa que o registro é adicionado à sessão (sem commit)."""
        service = AuditService(in_memory_db)

        audit_log = service.record(
            action="create",
            resource="assignment",
            user=admin_user,
            resource_id=1,
            after={"doctor_id": 123},
        )

        # O registro está na sessão (não foi commitado ainda)
        assert audit_log in in_memory_db.new


class TestAuditServiceRecordMany:
    """Testes da gravação em lote."""

    def test_record_many_creates_multiple_entries(self, in_memory_db: Session, admin_user: User):
        """Testa que record_many cria múltiplos registros."""
        service = AuditService(in_memory_db)

        entries = [
            {
                "action": "create",
                "resource": "assignment",
                "user": admin_user,
                "resource_id": 1,
                "after": {"doctor_id": 100},
                "period_id": 1,
            },
            {
                "action": "create",
                "resource": "assignment",
                "user": admin_user,
                "resource_id": 2,
                "after": {"doctor_id": 101},
                "period_id": 1,
            },
        ]

        audit_logs = service.record_many(entries)

        assert len(audit_logs) == 2
        assert audit_logs[0].resource_id == 1
        assert audit_logs[1].resource_id == 2


class TestAuditServiceQueryAuditLogs:
    """Testes da consulta de auditoria."""

    def test_query_filters_by_user_id(self, in_memory_db: Session, admin_user: User):
        """Testa filtro por user_id."""
        service = AuditService(in_memory_db)

        # Cria 2 registros com admin_user
        service.record("create", "assignment", admin_user, 1, after={"doctor_id": 100})
        service.record("create", "assignment", admin_user, 2, after={"doctor_id": 101})

        # Cria 1 registro com origem=system
        service.record("create", "assignment", None, 3, after={"doctor_id": 102})

        in_memory_db.commit()

        # Filtra por user_id
        page = service.query_audit_logs(user_id=admin_user.id)

        assert page.total == 2
        assert page.items[0].user_id == admin_user.id
        assert page.items[1].user_id == admin_user.id

    def test_query_filters_by_resource(self, in_memory_db: Session, admin_user: User):
        """Testa filtro por tipo de recurso."""
        service = AuditService(in_memory_db)

        service.record("create", "assignment", admin_user, 1, after={})
        service.record("create", "shift_extra", admin_user, 1, after={})

        in_memory_db.commit()

        page = service.query_audit_logs(resource="assignment")

        assert page.total == 1
        assert page.items[0].resource == "assignment"

    def test_query_filters_by_resource_id(self, in_memory_db: Session, admin_user: User):
        """Testa filtro por id do recurso."""
        service = AuditService(in_memory_db)

        service.record("create", "assignment", admin_user, 100, after={})
        service.record("create", "assignment", admin_user, 101, after={})

        in_memory_db.commit()

        page = service.query_audit_logs(resource_id=100)

        assert page.total == 1
        assert page.items[0].resource_id == 100

    def test_query_orders_by_occurred_at_desc(self, in_memory_db: Session, admin_user: User):
        """Testa que a ordenação é mais recente primeiro (DESC)."""
        service = AuditService(in_memory_db)

        # Cria 3 registros
        log1 = service.record("create", "assignment", admin_user, 1, after={})
        log2 = service.record("create", "assignment", admin_user, 2, after={})
        log3 = service.record("create", "assignment", admin_user, 3, after={})

        in_memory_db.commit()

        page = service.query_audit_logs()

        # Último criado deve vir primeiro (occurred_at DESC)
        assert page.items[0].id == log3.id
        assert page.items[1].id == log2.id
        assert page.items[2].id == log1.id

    def test_query_paginates(self, in_memory_db: Session, admin_user: User):
        """Testa paginação."""
        service = AuditService(in_memory_db)

        for i in range(1, 26):
            service.record("create", "assignment", admin_user, i, after={})

        in_memory_db.commit()

        page1 = service.query_audit_logs(page=1, size=10)
        page2 = service.query_audit_logs(page=2, size=10)

        assert page1.total == 25
        assert len(page1.items) == 10
        assert len(page2.items) == 10
        # Página 2 começa onde página 1 termina
        assert page1.items[-1].id != page2.items[0].id
