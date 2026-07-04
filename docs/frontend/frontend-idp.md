# Frontend IDP — Plantão 360

**Date:** 2026-06-27
**Status:** ✅ COMPLETE

---

## Visão Geral

O Frontend IDP (Internal Developer Platform) é o conjunto de ferramentas que governam o desenvolvimento frontend.

---

## Ferramentas

### 1. Feature Generator
- **Arquivo:** `tools/feature_generator.py`
- **Uso:** `python tools/feature_generator.py Period`
- **Função:** Gera feature completa automaticamente

### 2. Architecture Validator
- **Arquivo:** `tools/validate_frontend.py`
- **Uso:** `python tools/validate_frontend.py [feature]`
- **Função:** Valida estrutura, imports, naming

### 3. Frontend Score
- **Arquivo:** `tools/frontend_score.py`
- **Uso:** `python tools/frontend_score.py [feature]`
- **Função:** Calcula score de qualidade

### 4. Component Catalog
- **Arquivo:** `tools/component_catalog.py`
- **Uso:** `python tools/component_catalog.py`
- **Função:** Gera catálogo de componentes

### 5. Template Drift Detector
- **Arquivo:** `tools/template_drift.py`
- **Uso:** `python tools/template_drift.py [feature]`
- **Função:** Detecta divergências do Golden Module

### 6. Golden Lock Validator
- **Arquivo:** `tools/golden_lock.py`
- **Uso:** `python tools/golden_lock.py [feature]`
- **Função:** Valida compliance com Golden Lock

### 7. UX Validator
- **Arquivo:** `tools/ux_validator.py`
- **Uso:** `python tools/ux_validator.py [feature]`
- **Função:** Valida padrões UX

### 8. Manifest Validator
- **Arquivo:** `tools/manifest_validator.py`
- **Uso:** `python tools/manifest_validator.py [feature]`
- **Função:** Valida manifests

### 9. Template Sync
- **Arquivo:** `tools/template_sync.py`
- **Uso:** `python tools/template_sync.py`
- **Função:** Sincroniza templates com Golden Module

### 10. Frontend Review
- **Arquivo:** `tools/frontend_review.py`
- **Uso:** `python tools/frontend_review.py`
- **Função:** Gera relatório de review

### 11. CLI
- **Arquivo:** `tools/cli.py`
- **Uso:** `python tools/cli.py <command>`
- **Função:** CLI unificada

---

## Comandos CLI

```bash
# Criar feature
python tools/cli.py feature:create Period

# Validar features
python tools/cli.py validate

# Calcular score
python tools/cli.py score

# Gerar catálogo
python tools/cli.py catalog

# Detectar drift
python tools/cli.py drift

# Validar golden lock
python tools/cli.py golden-lock

# Validar UX
python tools/cli.py ux-validate

# Validar manifests
python tools/cli.py manifest-validate

# Gerar review
python tools/cli.py review

# Sincronizar templates
python tools/cli.py sync-templates
```

---

## Referências

- `tools/` — Todas as ferramentas
- `docs/frontend/golden-lock.md`
- `docs/frontend/feature-maturity.md`
