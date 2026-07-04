# Feature Maturity — Plantão 360

**Date:** 2026-06-27

---

## Levels

### Experimental
- Feature em fase inicial
- Pode mudar drasticamente
- Não deve ser usada em produção

### Alpha
- Feature com estrutura básica
- Funcionalidade parcial
- Pode conter bugs
- Pronta para testes internos

### Beta
- Feature com funcionalidade completa
- Testes básicos passando
- Pronta para testes de aceitação

### Production Ready
- Feature completa e testada
- Documentação completa
- Acessibilidade implementada
- Pronta para produção

### Golden
- Feature de referência
- Padrão oficial
- Todos os testes passando
- Documentação completa
- Acessibilidade completa

---

## Current Features

| Feature | Maturity | Owner |
|---|---|---|
| doctor | golden | unassigned |
| period | alpha | unassigned |
| shift | alpha | unassigned |
| assignment | alpha | unassigned |
| extra | alpha | unassigned |
| coverage | alpha | unassigned |
| payroll | alpha | unassigned |
| dashboard | alpha | unassigned |
| analytics | alpha | unassigned |
| readiness | alpha | unassigned |

---

## Process

Para promover uma feature de nível:
1. Implementar todas as funcionalidades
2. Criar testes unitários e de integração
3. Implementar acessibilidade
4. Criar documentação
5. Rodar validators (UX, Architecture, Golden Lock)
6. Atingir score mínimo (80 para Beta, 90 para Production Ready)
7. Aprovação no review

---

## Referências

- `tools/frontend_score.py`
- `tools/validate_frontend.py`
- `tools/golden_lock.py`
