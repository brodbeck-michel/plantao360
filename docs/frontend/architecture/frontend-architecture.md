# Frontend Architecture — Plantão 360

**Sprint:** 12 — Frontend Architecture, Enterprise Foundation & Golden Frontend Platform
**Data:** 2026-06-27

---

## Visão Geral

Arquitetura Feature-Based para o Frontend React Enterprise do Plantão 360.

---

## Estrutura de Diretórios

```
src/
├── app/                    # Configuração da aplicação
│   ├── App.tsx             # Componente raiz
│   └── main.tsx            # Entry point
├── features/               # Features por domínio
│   ├── doctor/             # Golden Module
│   ├── period/
│   ├── shift/
│   ├── assignment/
│   ├── extra/
│   ├── coverage/
│   ├── payroll/
│   ├── dashboard/
│   ├── analytics/
│   └── readiness/
├── shared/                 # Componentes e hooks compartilhados
│   ├── components/         # Componentes reutilizáveis
│   ├── hooks/              # Hooks compartilhados
│   ├── utils/              # Utilitários
│   ├── types/              # Tipos compartilhados
│   └── constants/          # Constantes
├── layouts/                # Layouts da aplicação
├── routes/                 # Definição de rotas
├── providers/              # Providers (Query, Theme, etc.)
├── hooks/                  # Hooks globais
├── services/               # Serviços e factories
├── api/                    # Cliente HTTP
├── theme/                  # Design tokens e tema
├── types/                  # Tipos globais
└── assets/                 # Imagens, ícones, etc.
```

---

## Justificativa por Diretório

### `features/`
Cada feature é um módulo independente contendo:
- `components/` — Componentes da feature
- `hooks/` — Hooks específicos
- `services/` — API e lógica de dados
- `types/` — Tipos específicos
- `pages/` — Páginas (tela completa)

**Por quê?** Organização por domínio facilita manutenção e escalabilidade.

### `shared/`
Componentes e hooks usados por múltiplas features.

**Por quê?** Evita duplicação e garante consistência.

### `layouts/`
Layouts da aplicação (sidebar, toolbar, etc.).

**Por quê?** Separar layout de conteúdo facilita mudanças visuais.

### `routes/`
Definição centralizada de rotas.

**Por quê?** Uma única fonte de verdade para navegação.

### `providers/`
Providers React (Query, Theme, Auth).

**Por quê?** Composição limpa e testável.

### `services/`
Query keys, factories e serviços globais.

**Por quê?** Infraestrutura compartilhada entre features.

### `api/`
Cliente HTTP e configuração.

**Por quê?** Abstração do Axios. Nenhum componente importa Axios.

### `theme/`
Design tokens e tema MUI.

**Por quê?** Tokens centralizados garantem consistência visual.

### `types/`
Tipos TypeScript globais.

**Por quê?** Tipos compartilhados entre todas as features.

---

## Regras de Importação

### Permitido
- Feature → Shared
- Feature → Services
- Feature → API
- Feature → Types
- Shared → API
- Shared → Types

### Proibido
- Feature → Feature (acoplamento)
- Shared → Feature (inversão)
- Qualquer módulo → Axios (abstração)
- Qualquer módulo → URL hardcoded (abstração)

---

## Validação

| Critério | Status |
|---|---|
| Estrutura definida | ✅ |
| Justificativa documentada | ✅ |
| Regras de importação definidas | ✅ |
| Pronto para 20+ módulos | ✅ |
