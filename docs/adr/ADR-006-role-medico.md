# ADR-006: Role MEDICO

## Status

Aceito

## Data

2026-06-24

## Contexto

Os perfis atuais definidos no RBAC são:

- ADMIN
- COORDENADOR
- FINANCEIRO
- CONSULTA

## Problema

Médicos provavelmente terão acesso próprio ao sistema no futuro, com permissões específicas como visualização de suas próprias escalas, histórico de plantões e dados pessoais. Usar o perfil CONSULTA seria insuficiente pois não permite ações como confirmar presença em plantão ou visualizar dados sensíveis do médico.

## Decisão

Criar o papel `MEDICO` desde a fundação do RBAC, mesmo antes da implementação completa de autenticação.

## Consequências

### Positivas
- Evita migração de perfis futura
- Facilita implementação de autenticação por papéis
- Mantém consistência com a documentação do sistema

### Negativas
- Papel não utilizado ainda (over-engineering mínimo)

## Alternativas Descartadas

1. **Criar apenas quando houver autenticação**: Risco de esquecer ou criar inconsistências
2. **Usar CONSULTA para médicos**: Permissões insuficientes para ações futuras do médico
