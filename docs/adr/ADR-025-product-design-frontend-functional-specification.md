# ADR-025: Product Design & Frontend Functional Specification

**Date:** 2026-06-27
**Status:** Accepted
**Sprint:** 11

---

## Context

O Plantão 360 completou a fase de aplicação com o backend congelado e o domínio congelado. A próxima fase é a implementação do Frontend React.

Antes de implementar código React, é necessário modelar completamente a experiência do usuário, garantindo que:

1. Todas as personas estejam documentadas
2. Todas as jornadas estejam completas
3. Todas as telas estejam especificadas
4. Todas as regras de UX estejam definidas
5. Todos os contratos estejam mapeados
6. Todos os erros estejam documentados
7. Todas as permissões estejam mapeadas
8. Todas as metas de performance estejam definidas
9. A estratégia mobile esteja clara

---

## Decision

Declaramos a **Product Design & Frontend Functional Specification** completa com os seguintes elementos:

### 1. Auditoria Funcional
- 0 operações sem suporte
- 0 APIs inutilizadas
- 3 jornadas faltantes identificadas (Extras, Relatórios, Exportação)
- 0 regras impossíveis
- 2 operações de alta complexidade identificadas

### 2. Personas
- 7 personas documentadas: Coordenador, Médico, Financeiro, RH, Auditor, Administrador, Diretor
- Cada uma com responsabilidades, objetivos, dores, frequência, dispositivos, nível técnico, indicadores, permissões, operações críticas

### 3. User Journeys Detalhadas
- 7 jornadas completas com BPMN
- Fluxos de início, objetivo, decisões, exceções, erros, dependências, finalização

### 4. Task Flows
- 9 tarefas documentadas
- Passos, tempo esperado, frequência, criticidade

### 5. Screen Inventory
- 28 telas especificadas
- Cada uma com objetivo, persona, dados, endpoints, KPIs, Read Models, Queries, Explainability, permissões

### 6. Navegação
- Menu lateral estruturado
- Breadcrumbs definidos
- Atalhos documentados
- Deep links definidos
- Navegação contextual mapeada

### 7. UX Rules
- 25 regras definidas
- Gerais, tabelas, formulários, dialogs, notificações, keyboard

### 8. Design System Functional
- 30 componentes funcionais
- Tabelas, formulários, filtros, timelines, cards, alertas, indicadores, diálogos

### 9. Frontend Contract Matrix
- 54 contratos mapeados
- 32 DTOs, 13 Queries, 12 Read Models, 8 KPIs, 7 Explainability

### 10. Error Experience
- 22 mensagens de erro/sucesso
- Validação, estado, negócio, sistema, permissão, sucesso

### 11. Access Matrix
- 7 personas × 28 telas mapeadas
- Botões, ações, endpoints, permissões

### 12. Performance Goals
- 10 categorias de performance
- Metas mensuráveis e estratégias

### 13. Mobile Strategy
- Funcionalidades mobile definidas
- Jornadas mobile first (Médico)
- Jornadas desktop (Coordenador, Financeiro)
- Responsividade, offline, push notifications

### 14. Frontend Readiness
- Backend suporta 100% das telas
- 0 lacunas identificadas

---

## Consequences

### Positivas

1. **Especificação completa** — Equipe pode implementar sem reinterpretar regras
2. **Consistência** — Todas as telas seguem mesmas regras
3. **Testabilidade** — Contratos permitem testes de integração
4. **Manutenibilidade** — Documentação facilita mudanças futuras
5. **Onboarding** — Nova equipe pode começar imediatamente

### Negativas

1. **Volume de documentação** — Muitos documentos para manter
2. **Rigidez** — Mudanças requerem atualização em múltiplos documentos
3. **Tempo de preparo** — Sprint longa de modelagem

### Neutras

1. **Documentação viva** — Pode ser atualizada conforme necessidade
2. **Flexibilidade** — Regras podem ser ajustadas se necessário

---

## Pergunta Fundamental

> **"Se eu remover todo o código React do projeto hoje, ainda assim será possível reconstruir toda a interface apenas utilizando a documentação produzida nesta sprint?"**

**Resposta:** SIM.

Toda a interface pode ser reconstruída apenas com a documentação produzida:
- Personas definem quem usa
- Journeys definem como usam
- Screen Inventory define o quê é exibido
- Frontend Contract Matrix define os dados
- UX Rules definem o comportamento
- Access Matrix define permissões
- Error Experience define mensagens
- Performance Goals definem metas
- Mobile Strategy define dispositivos

---

## References

- `docs/product/reviews/functional-audit.md`
- `docs/product/personas.md`
- `docs/product/user-journeys-detailed.md`
- `docs/product/task-flows.md`
- `docs/frontend/screen-inventory.md`
- `docs/frontend/navigation-map.md`
- `docs/frontend/ux-rules.md`
- `docs/frontend/design-system-functional.md`
- `docs/frontend/frontend-contract-matrix.md`
- `docs/frontend/error-experience.md`
- `docs/frontend/access-matrix.md`
- `docs/frontend/performance-goals.md`
- `docs/frontend/mobile-strategy.md`
- `docs/reviews/frontend-readiness.md`
