# Doctor Frontend Guide — Plantão 360

**Sprint:** 13 — Golden Frontend Module
**Data:** 2026-06-27

---

## Visão Geral

O módulo Doctor é o **Golden Frontend Module** — referência oficial para todas as futuras features do Plantão 360.

---

## Estrutura

```
features/doctor/
├── api/                    # (reservado para API-specific)
├── components/             # Componentes reutilizáveis da feature
│   ├── doctor-avatar.tsx   # Avatar de médico
│   ├── doctor-card.tsx     # Card de médico
│   ├── doctor-header.tsx   # Cabeçalho da página
│   └── doctor-toolbar.tsx  # Toolbar da página
├── dialogs/                # Diálogos de ação
│   ├── doctor-create-dialog.tsx
│   ├── doctor-edit-dialog.tsx
│   ├── doctor-delete-dialog.tsx
│   └── doctor-deactivate-dialog.tsx
├── details/                # Painéis de detalhes
│   └── doctor-details-panel.tsx
├── filters/                # Filtros reutilizáveis
│   └── doctor-filter-bar.tsx
├── forms/                  # Formulários
│   └── doctor-form.tsx
├── hooks/                  # Hooks de negócio
│   └── use-doctors.ts
├── history/                # Timeline de histórico
│   └── doctor-history-timeline.tsx
├── audit/                  # Card de auditoria
│   └── doctor-audit-card.tsx
├── pages/                  # Páginas completas
│   ├── doctor-list-page.tsx
│   ├── doctor-detail-page.tsx
│   ├── doctor-history-page.tsx
│   ├── doctor-audit-page.tsx
│   └── doctor-profile-drawer.tsx
├── services/               # API e mutations
│   └── doctor-api.ts
├── tables/                 # Tabelas
│   └── doctor-table.tsx
├── types/                  # Tipos
│   └── doctor-types.ts
├── utils/                  # Utilitários
├── manifest/               # Manifest da feature
├── tests/                  # Testes
└── index.ts                # Barrel file
```

---

## Convenções

### Naming
- **Component:** PascalCase (`DoctorCard`)
- **File:** kebab-case (`doctor-card.tsx`)
- **Hook:** camelCase com prefixo `use` (`useDoctorList`)
- **Type:** PascalCase (`DoctorFilters`)
- **Route:** kebab-case (`/app/doctors/:id`)

### Imports
1. React (se necessário)
3. Shared Components
4. Types
5. Hooks

### Exports
- Named exports apenas
- Barrel file (`index.ts`) para API pública

---

## Uso como Referência

Para criar uma nova feature, copie a estrutura do Doctor:

```bash
cp -r features/doctor features/[new-feature]
# Renomear arquivos e componentes
```

---

## Referências

- `docs/frontend/entity-page-blueprint.md`
- `docs/frontend/architecture/component-guidelines.md`
- `docs/frontend/architecture/api-guide.md`
