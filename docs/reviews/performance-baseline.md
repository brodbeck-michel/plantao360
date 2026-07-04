# Performance Baseline

**Date:** 2026-06-25

**Status:** Active

---

## Overview

This document establishes performance baselines for Plantão 360.

Use these baselines to track performance degradation over time.

## Build Performance

| Metric | Baseline | Target |
|--------|----------|--------|
| Docker Build (clean) | - | < 120s |
| Docker Build (cached) | - | < 30s |
| pip install | - | < 60s |

## Test Performance

| Metric | Baseline | Target |
|--------|----------|--------|
| Unit Tests (all) | - | < 30s |
| Integration Tests | - | < 60s |
| Contract Tests | - | < 30s |
| Full Test Suite | - | < 120s |

## Code Generation

| Metric | Baseline | Target |
|--------|----------|--------|
| Module Generator | - | < 5s |
| ADR Generator | - | < 1s |
| Documentation Generator | - | < 5s |
| Compliance Report | - | < 10s |

## Code Quality

| Metric | Baseline | Target |
|--------|----------|--------|
| Total Lines | 4,817 | - |
| Test Functions | 54 | - |
| Coverage | - | ≥ 80% |
| Architecture Score | 100% | 100% |

## Module Statistics

| Metric | Value |
|--------|-------|
| Total Modules | 6 |
| Golden Modules | 1 (Doctor) |
| Models | 6 |
| Services | 1 |
| Repositories | 1 |
| DTOs | 7 |
| Endpoints | 5 |
| Test Files | 8 |
| Test Functions | 54 |

## Monitoring

Run periodically to track changes:

```bash
python tools/project_metrics.py
python tools/validate_architecture.py --all
python tools/lint_architecture.py
```

## Thresholds

| Metric | Warning | Critical |
|--------|---------|----------|
| Test Duration | > 60s | > 120s |
| Coverage | < 80% | < 70% |
| Architecture Score | < 100% | < 90% |
| Lint Errors | > 0 | > 5 |
| TODOs | > 50 | > 100 |
