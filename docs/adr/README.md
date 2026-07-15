# ADRs — Registro histórico (superado pela Constituição)

> ⚠️ **Estes 31 ADRs são registro histórico.** A
> [Constituição do projeto](../../.specify/memory/constitution.md) (v1.1.0, 2026-07-13) **supera**
> os ADRs onde houver conflito — em especial os de *freeze* (ADR-017, ADR-024, ADR-031) e toda a
> arquitetura DDD tático / CQRS / event-sourcing que eles ratificaram. Não são removidos: contam a
> história de como o sistema chegou aqui.

## Por que estão superados

O backend nasceu super-engenhariado (~25k linhas, 495 arquivos, camada `domain/` com 118 arquivos
em DDD/CQRS/event-sourcing/aggregate-roots). A partir de 2026-07, o projeto adotou o princípio
**"simples, mas bem feito"** (Constituição, Princípio I — Simplicidade Deliberada) e desmontou essa
arquitetura de forma incremental e com paridade funcional:

- **spec 003** — baseline de testes (rede de segurança para simplificar).
- **spec 004 / 005** — colapso da `domain/`: 118 → 32 arquivos (inline-and-delete de abstrações de
  consumidor único, remoção de motores/read-models/state-machines mortos).
- **spec 006** — remoção da superfície payroll/cobertura sem uso (nenhuma tela a consumia) + o
  cluster `domain/` restante + o pacote `integrations/`. `domain/` final: ~13 arquivos, só
  fundação (constants/errors/events/exceptions).

Resultado: a `domain/` deixou de ser uma camada de cerimônia e passou a `rota → service → model`.
Os ADRs que ratificaram a arquitetura antiga (padrões enterprise, agregados, governança, golden
module, freezes) descrevem um estado que **não existe mais no código**.

## Como ler estes ADRs

- Para **entender uma decisão de produto/domínio** ainda vigente (papéis, auto-escala, extras sem
  aprovação prévia, competência 26→25), veja `specs/001-baseline-funcional/`.
- Para **regras de arquitetura vigentes**, a fonte única é a
  [Constituição](../../.specify/memory/constitution.md), não os ADRs.
- Os ADRs abaixo permanecem apenas como rastro histórico (cada um leva um aviso no topo).

## Índice

| ADR | Tema | Situação |
|-----|------|----------|
| 001 | Monolito modular | Base ainda válida (mono-serviço); detalhes superados |
| 002 | Clean Architecture | Superado (camadas colapsadas) |
| 003 | FastAPI + React | **Vigente** (stack mantida na Constituição) |
| 004 | SQLite dev / Postgres prod | **Vigente** (Constituição, Princípio IV) |
| 005 | Service layer | Parcialmente vigente (rota→service→model) |
| 006 | Papel Médico | Vigente como produto (ver spec 001) |
| 007 | Identificadores distribuídos | Superado |
| 008 | Domain constants | Parcialmente vigente (constants sobrevivem) |
| 009 | Unicidade de plantão | Vigente como regra (inline no service) |
| 010 | Enterprise application patterns | Superado (removido nas specs 004–006) |
| 011 | Platform governance | Superado |
| 012 | Period aggregate | Superado (agregado desmontado) |
| 013 | Domain core | Superado |
| 014 | Shift aggregate | Superado |
| 015 | Assignment domain | Superado |
| 016 | Module manifest | Superado (tooling removido na Fase 3) |
| 017 | **Engineering freeze** | Superado (freeze revogado pela Constituição) |
| 018 | Extras de plantão | Vigente como produto (ver spec 001) |
| 019 | Fundação domínio financeiro | Superado (removido na spec 006) |
| 020 | Motor de remuneração | Superado (removido — folha é do ERP) |
| 021 | Competência financeira | Superado (removido na spec 006) |
| 022 | Governança administrativa | Superado (removido na spec 006) |
| 023 | Query domain / explainability | Superado (removido na spec 006) |
| 024 | **Domain freeze** / integration architecture | Superado (freeze revogado; `integrations/` removido) |
| 025 | Product design / frontend spec | Parcialmente vigente (produto) |
| 026 | Frontend enterprise architecture | Superado em parte |
| 027 | Golden frontend module | Superado (golden guard removido) |
| 028 | Frontend platform governance | Superado |
| 029 | Production readiness | Vigente em espírito (ver `docs/deploy.md` + Constituição IV) |
| 030 | Operational user experience | Vigente como produto |
| 031 | **Operational core frozen** | Superado (freeze revogado) |

> Novas decisões de arquitetura **não** entram como ADR. A Constituição é a fonte única; mudanças
> relevantes passam pelo fluxo Spec Kit (`specify → plan → tasks → implement`) em `specs/`.
