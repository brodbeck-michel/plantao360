# CLAUDE.md — Plantão 360

Este arquivo **não repete** as regras gerais de infraestrutura, Git, Azure
DevOps ou identidade visual da Unimed Tubarão — todas estão em
`/home/michelmendes/projetos/Unimed/.claude/CLAUDE.md` e valem aqui sem
exceção, salvo o registrado na seção "Pendências" abaixo.

## O que é

Sistema de gestão de plantões médicos para intranet da Unimed Tubarão:
períodos de escala, atribuição de plantonistas, horas extras, fechamento e
auditoria de período.

## Stack

- **Backend:** FastAPI + SQLAlchemy 2.x + Alembic, Python 3.12. Testes com
  pytest (gate de cobertura 65%, ver `pyproject.toml`).
- **Frontend:** React 18 + Vite + TypeScript.
- **Banco:** PostgreSQL 16 (container `db` no `docker-compose.yml`).
- **Deploy:** imagens publicadas no GHCR (`ghcr.io/brodbeck-michel/plantao360-*`)
  via `.github/workflows/release-images.yml`, disparado por tag `vX.Y.Z`. O
  servidor nunca compila — só `docker compose pull && up -d`. Detalhes em
  `docs/runbook-deploy.md`.

## Domínio — onde procurar

- Glossário e regras de negócio: `docs/domain/` (glossário por área:
  `glossario-financeiro.md`, `glossario-payroll.md`, `glossario-governanca.md`,
  `glossario-consultas.md`, `glossario-extras.md`; mapa de contexto em
  `context-map.md`).
- Especificações por feature: `specs/<NNN-nome>/` (Spec Kit — feature ativa em
  `.specify/feature.json`).
- Relatórios de conformidade/dívida técnica: `docs/reports/`.

## Repositório

- GitHub: `brodbeck-michel/plantao360` — é a fonte da verdade (regra "projeto
  que já roda no GitHub continua no GitHub", ver CLAUDE.md global §4).
- Branch principal: `main` (renomeada de `master` em 2026-09-13, sem branch
  protegida configurada — nenhuma aprovação obrigatória via GitHub hoje; a
  exigência de aprovação por resumo em português, antes do merge, é processo,
  não gate técnico).
- CI (`.github/workflows/ci.yml`) roda em `main`. Release de imagens
  (`release-images.yml`) dispara em tag `v*`.
- Sem espelho no Azure DevOps ainda — pendente, ver abaixo.

## Pendências de adequação ao padrão Unimed (não resolvidas nesta sessão)

Registradas aqui para não se perderem; cada uma exige decisão/alinhamento
antes de mexer, por afetar produção:

1. **Container de banco na stack de produção/homologação.** O
   `docker-compose.yml` atual sobe o serviço `db` (Postgres) na própria stack,
   inclusive em produção. O padrão global (§1) diz que homolog/produção nunca
   sobem banco no compose — conectam a um cluster já provisionado via
   `DATABASE_URL` externa. Migrar isso exige: provisionar o Plantão 360 no
   cluster Postgres da infra, decidir janela de migração de dados do container
   atual, e só então remover o serviço `db` do compose. Não fazer sem
   alinhamento prévio com infraestrutura.
2. **Nomenclatura do banco.** Hoje `POSTGRES_DB=plantao360` /
   `POSTGRES_USER=plantao360`. O padrão é `db_plantao360` (produção) /
   `db_plantao360_hml` / `db_plantao360_local` e usuário `usr_plantao360`.
   Renomear só faz sentido junto com o item 1 (migração para cluster externo),
   para não trocar nome duas vezes.
3. **Espelho Azure DevOps.** Falta o workflow
   `.github/workflows/mirror-azure.yml` (push de branches/tags a cada push em
   `main`, força-empurrado, ver modelo já descrito no CLAUDE.md global §4) e o
   segredo `AZURE_DEVOPS_PAT` no repositório GitHub. Precisa que alguém gere o
   PAT (escopo *Code read & write*) no Azure DevOps — não é algo que se
   resolve só no código.

## Observabilidade (CLAUDE.md global §7)

Não se aplica hoje: o projeto não chama API externa, HUB de API nem sistema
core (TASY/Protheus/SGU/Senior). Existe a flag `ENABLE_TASY_INTEGRATION` em
`backend/app/core/features.py`, mas desligada por padrão e sem integração
implementada. **Se essa integração for ativada no futuro, a seção 7 do
CLAUDE.md global passa a valer** (logging de início/sucesso/falha + tabela
`job_queue` para chamadas assíncronas) — implementar junto com a integração,
não depois.

## Higiene de arquivos

- `.gitattributes` força `eol=lf` em todo o repositório — arquivos editados a
  partir de ambiente Windows (inclusive via drive de rede, ver
  `docs/HANDOFF.md`) não devem mais gerar diff de CRLF↔LF. Se aparecer diff
  gigante mudando só fim de linha, é sinal de que algo ignorou o
  `.gitattributes` (editor sem suporte, ou arquivo herdado de antes dele
  existir) — não commitar, rodar `git checkout -- <arquivo>` e investigar.
