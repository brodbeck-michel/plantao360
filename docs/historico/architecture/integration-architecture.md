# Integration Architecture — Plantão 360

**Sprint:** 10.5 — Domain Freeze, Application Baseline & Integration Architecture
**Data:** 2026-06-27

---

## Visão Geral

A Integration Architecture define como o Plantão 360 se integra com sistemas externos, mantendo o domínio completamente desacoplado.

---

## Princípios

1. **Domínio é independente** — Domain não conhece sistemas externos
2. **Contratos definem interfaces** — Integration Contracts definem o que é possível
3. **Adapters implementam** — External Adapters implementam contratos
4. **ACL protege** — Anti-Corruption Layer traduz dados externos

---

## Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                      Domain Layer                        │
│  (Nunca importa sistemas externos)                       │
├─────────────────────────────────────────────────────────┤
│                 Integration Contracts                    │
│  (Interfaces que definem capacidades)                    │
├─────────────────────────────────────────────────────────┤
│                 Anti-Corruption Layer                    │
│  (Traduz dados externos para formato do domínio)         │
├─────────────────────────────────────────────────────────┤
│                 External Adapters                        │
│  (Implementam contratos para sistemas específicos)       │
├─────────────────────────────────────────────────────────┤
│                 External Systems                         │
│  (Tasy, MV Soul, TOTVS, SAP, Senior, Banking)           │
└─────────────────────────────────────────────────────────┘
```

---

## Integration Contracts

### 1. HospitalAdapter

```python
class HospitalAdapter(Protocol):
    async def get_hospital(self, hospital_id: str) -> HospitalData: ...
    async def list_hospitals(self) -> list[HospitalData]: ...
    async def get_hospital_schedule(self, hospital_id: str, date: date) -> ScheduleData: ...
```

---

### 2. PayrollAdapter

```python
class PayrollAdapter(Protocol):
    async def export_payroll(self, payroll_id: str, data: PayrollExportData) -> ExportResult: ...
    async def import_payroll(self, file_path: str) -> PayrollImportData: ...
    async def get_payroll_status(self, payroll_id: str) -> PayrollExternalStatus: ...
```

---

### 3. DoctorAdapter

```python
class DoctorAdapter(Protocol):
    async def sync_doctors(self) -> SyncResult: ...
    async def get_doctor(self, doctor_id: str) -> DoctorExternalData: ...
    async def validate_crm(self, crm: str) -> CRMValidationResult: ...
```

---

### 4. ScheduleAdapter

```python
class ScheduleAdapter(Protocol):
    async def export_schedule(self, period_id: str) -> ScheduleExportData: ...
    async def import_schedule(self, file_path: str) -> ScheduleImportData: ...
    async def get_schedule_conflicts(self, period_id: str) -> list[ConflictData]: ...
```

---

### 5. FinancialAdapter

```python
class FinancialAdapter(Protocol):
    async def export_financial(self, period_id: str) -> FinancialExportData: ...
    async def import_financial(self, file_path: str) -> FinancialImportData: ...
    async def get_payment_status(self, doctor_id: str) -> PaymentStatusData: ...
```

---

### 6. NotificationAdapter

```python
class notificationAdapter(Protocol):
    async def send_notification(self, notification: NotificationData) -> NotificationResult: ...
    async def send_email(self, email: EmailData) -> EmailResult: ...
    async def send_sms(self, sms: SMSData) -> SMSResult: ...
```

---

## Anti-Corruption Layer

### Estrutura

```
backend/app/integrations/
├── acl/
│   ├── __init__.py
│   ├── hospital_acl.py
│   ├── payroll_acl.py
│   ├── doctor_acl.py
│   ├── schedule_acl.py
│   ├── financial_acl.py
│   └── notification_acl.py
```

### Padrão

```python
class HospitalACL:
    def __init__(self, adapter: HospitalAdapter):
        self._adapter = adapter

    async def get_hospital(self, hospital_id: str) -> Hospital:
        external_data = await self._adapter.get_hospital(hospital_id)
        return self._to_domain(external_data)

    def _to_domain(self, external_data: HospitalData) -> Hospital:
        # Traduz dados externos para formato do domínio
        return Hospital(
            id=external_data.id,
            name=external_data.name,
            address=external_data.address
        )
```

---

## External Adapters

### Estrutura

```
backend/app/integrations/adapters/
├── __init__.py
├── hospital_adapter.py
├── payroll_adapter.py
├── doctor_adapter.py
├── schedule_adapter.py
├── financial_adapter.py
├── notification_adapter.py
├── tasy_adapter.py
├── mvsoul_adapter.py
├── totvs_adapter.py
├── sap_adapter.py
└── senior_adapter.py
```

---

## Integration Providers

### Estrutura

```
backend/app/integrations/providers/
├── __init__.py
├── hospital_provider.py
├── payroll_provider.py
├── doctor_provider.py
├── schedule_provider.py
├── financial_provider.py
└── notification_provider.py
```

---

## Data Mappers

### Estrutura

```
backend/app/integrations/mappers/
├── __init__.py
├── hospital_mapper.py
├── payroll_mapper.py
├── doctor_mapper.py
├── schedule_mapper.py
├── financial_mapper.py
└── notification_mapper.py
```

---

## Sistemas Externos

### 1. Tasy (ERP Hospitalar)
- **Status:** FUTURO (não implementado)
- **Adapter:** `tasy_adapter.py` (placeholder)
- **Uso:** Integração com dados hospitalares

### 2. MV Soul (ERP Hospitalar)
- **Status:** FUTURO (não implementado)
- **Adapter:** `mvsoul_adapter.py` (placeholder)
- **Uso:** Integração com dados hospitalares

### 3. TOTVS (ERP)
- **Status:** FUTURO (não implementado)
- **Adapter:** `totvs_adapter.py` (placeholder)
- **Uso:** Integração com dados financeiros

### 4. SAP (ERP)
- **Status:** FUTURO (não implementado)
- **Adapter:** `sap_adapter.py` (placeholder)
- **Uso:** Integração com dados financeiros

### 5. Senior (ERP)
- **Status:** FUTURO (não implementado)
- **Adapter:** `senior_adapter.py` (placeholder)
- **Uso:** Integração com dados de folha

---

## Fluxo de Integração

### 1. Fluxo de Exportação

```
Domain → Application → Integration Contract → ACL → Adapter → External System
```

### 2. Fluxo de Importação

```
External System → Adapter → ACL → Integration Contract → Application → Domain
```

### 3. Fluxo de Sincronização

```
External System → Adapter → ACL → Integration Contract → Application → Domain Events → Projections
```

---

## Validação

| Critério | Status |
|---|---|
| Integration Contracts definidos | ✅ |
| Anti-Corruption Layer estruturada | ✅ |
| External Adapters estruturados | ✅ |
| Domain desacoplado | ✅ |
| Sistemas externos documentados | ✅ |
| Fluxos documentados | ✅ |
