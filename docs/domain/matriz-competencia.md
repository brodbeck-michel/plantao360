# Matriz da Competência — Payroll

**Sprint:** 9
**Data:** 2026-06-26

---

## Quem cria?

| Ação | Responsável | Condição |
|---|---|---|
| Criar competência | **Gestor de Escala** ou **Sistema** | Período fechado + nenhum cálculo existente |
| Iniciar cálculo | **Gestor de Escala** | Competência em estado `draft` |

## Quem aprova?

| Ação | Responsável | Condição |
|---|---|---|
| Revisar | **Gestor de Escala** | Competência em estado `calculated` |
| Aprovar | **Administrador Financeiro** | Competência em estado `reviewed` |
| Exportar | **Diretor** | Competência em estado `approved` |
| Marcar como pago | **Administrador Financeiro** | Competência em estado `exported` |

## Quem consulta?

| Ação | Responsável | Condição |
|---|---|---|
| Ver competência | Qualquer usuário autenticado | Sempre |
| Ver histórico | **Administrador Financeiro** | Sempre |
| Ver explicações | **Gestor de Escala** ou superior | Competência calculada |
| Ver selo | **Auditor** ou superior | Competência aprovada |

## Quem reabre?

| Ação | Responsável | Condição |
|---|---|---|
| Reabrir | **Administrador Financeiro** | Competência em estado `approved` ou `exported` |
| Justificativa | Obrigatória | Campo `reopen_reason` |

## Quem fecha?

| Ação | Responsável | Condição |
|---|---|---|
| Fechar competência | **Administrador Financeiro** | Competência em estado `paid` |
| Arquivar | **Sistema** | Após 30 dias em estado `paid` |

## Quem exporta?

| Ação | Responsável | Condição |
|---|---|---|
| Exportar para ERP | **Diretor** | Competência em estado `approved` |
| Gerar relatório | **Gestor de Escala** | Competência calculada |

---

## Regras de Transição

```
draft → calculated     (cálculo executado)
calculated → reviewed  (revisão concluída)
reviewed → approved    (aprovação formal)
approved → exported    (exportação para ERP)
exported → paid        (confirmação de pagamento)
paid → archived        (arquivamento automático)

Qualquer estado → reopened (reabertura, gera nova versão)
```

---

## Permissões por Papel

| Papel | Criar | Calcular | Revisar | Aprovar | Reabrir | Exportar | Arquivar |
|---|---|---|---|---|---|---|---|
| Gestor de Escala | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Administrador Financeiro | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| Diretor | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Auditor | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
