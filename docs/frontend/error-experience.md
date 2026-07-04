# Error Experience — Plantão 360

**Sprint:** 11 — Product Design, User Experience Modeling & Frontend Functional Specification
**Data:** 2026-06-27

---

## Visão Geral

Definição de mensagens de erro para todas as situações identificadas no domínio. NUNCA utilizar mensagens técnicas.

---

## 1. Erros de Validação

### ERR-001: Campo Obrigatório Ausente

| Propriedade | Valor |
|---|---|
| **Mensagem** | "O campo {nome} é obrigatório." |
| **Orientação** | "Preencha o campo {nome} para continuar." |
| **Ação Sugerida** | Preencher campo |
| **Impacto** | Baixo |
| **Recuperação** | Preencher campo e tentar novamente |

### ERR-002: Formato Inválido

| Propriedade | Valor |
|---|---|
| **Mensagem** | "O campo {nome} está com formato inválido." |
| **Orientação** | "Esperado: {formato}. Exemplo: {exemplo}" |
| **Ação Sugerida** | Corrigir formato |
| **Impacto** | Baixo |
| **Recuperação** | Ajustar formato e tentar novamente |

### ERR-003: CRM Já Cadastrado

| Propriedade | Valor |
|---|---|
| **Mensagem** | "Este CRM já está cadastrado no sistema." |
| **Orientação** | "Verifique se o médico já foi cadastrado ou use outro CRM." |
| **Ação Sugerida** | Buscar médico existente ou cadastrar com outro CRM |
| **Impacto** | Médio |
| **Recuperação** | Buscar médico ou usar CRM diferente |

### ERR-004: Período Sobreposto

| Propriedade | Valor |
|---|---|
| **Mensagem** | "Já existe um período com datas sobrepostas." |
| **Orientação** | "Ajuste as datas para evitar conflito com períodos existentes." |
| **Ação Sugerida** | Ajustar datas |
| **Impacto** | Médio |
| **Recuperação** | Modificar datas ou verificar período existente |

---

## 2. Erros de Estado

### ERR-005: Transição Não Permitida

| Propriedade | Valor |
|---|---|
| **Mensagem** | "Esta ação não é permitida no status atual." |
| **Orientação** | "Status atual: {status}. Ação permitida apenas em: {status permitido}" |
| **Ação Sugerida** | Verificar status e ações disponíveis |
| **Impacto** | Médio |
| **Recuperação** | Executar ação compatível com status atual |

### ERR-006: Período Fechado

| Propriedade | Valor |
|---|---|
| **Mensagem** | "Este período está fechado e não pode ser editado." |
| **Orientação** | "Para editar, reabra o período primeiro." |
| **Ação Sugerida** | Reabrir período |
| **Impacto** | Médio |
| **Recuperação** | Reabrir período antes de editar |

### ERR-007: Payroll Bloqueado

| Propriedade | Valor |
|---|---|
| **Mensagem** | "Esta competência está bloqueada e não pode ser alterada." |
| **Orientação** | "Contate o administrador para desbloquear." |
| **Ação Sugerida** | Contatar administrador |
| **Impacto** | Alto |
| **Recuperação** | Solicitar desbloqueio ao administrador |

### ERR-008: Checklist Incompleto

| Propriedade | Valor |
|---|---|
| **Mensagem** | "O checklist de aprovação está incompleto." |
| **Orientação** | "Complete todos os itens do checklist antes de aprovar." |
| **Ação Sugerida** | Completar checklist |
| **Impacto** | Médio |
| **Recuperação** | Preencher todos os itens obrigatórios |

---

## 3. Erros de Negócio

### ERR-009: Médico Já Atribuído

| Propriedade | Valor |
|---|---|
| **Mensagem** | "Este médico já está atribuído a um plantão neste horário." |
| **Orientação** | "Selecione outro médico ou ajuste o horário." |
| **Ação Sugerida** | Selecionar outro médico |
| **Impacto** | Médio |
| **Recuperação** | Escolher médico disponível |

### ERR-010: Cobertura Não Aprovável

| Propriedade | Valor |
|---|---|
| **Mensagem** | "Esta cobertura não pode ser aprovada no momento." |
| **Orientação** | "Status atual: {status}. Aprovação permitida apenas em PENDING." |
| **Ação Sugerida** | Verificar status da cobertura |
| **Impacto** | Baixo |
| **Recuperação** | Aguardar status correto ou verificar motivo |

### ERR-011: Readiness Não Atendido

| Propriedade | Valor |
|---|---|
| **Mensagem** | "A competência não atende os requisitos para processamento." |
| **Orientação** | "Verifique os itens de readiness pendentes." |
| **Ação Sugerida** | Resolver pendências de readiness |
| **Impacto** | Alto |
| **Recuperação** | Completar itens pendentes |

### ERR-012: Dados Financeiros Inconsistentes

| Propriedade | Valor |
|---|---|
| **Mensagem** | "Foram encontradas inconsistências nos dados financeiros." |
| **Orientação** | "Revise as inconsistências antes de processar." |
| **Ação Sugerida** | Revisar e resolver inconsistências |
| **Impacto** | Alto |
| **Recuperação** | Corrigir dados inconsistentes |

---

## 4. Erros de Sistema

### ERR-013: Falha de Conexão

| Propriedade | Valor |
|---|---|
| **Mensagem** | "Não foi possível conectar ao servidor." |
| **Orientação** | "Verifique sua conexão com a internet e tente novamente." |
| **Ação Sugerida** | Retry |
| **Impacto** | Alto |
| **Recuperação** | Verificar conexão e retry |

### ERR-014: Serviço Indisponível

| Propriedade | Valor |
|---|---|
| **Mensagem** | "O serviço está temporariamente indisponível." |
| **Orientação** | "Aguarde alguns minutos e tente novamente." |
| **Ação Sugerida** | Aguardar e retry |
| **Impacto** | Alto |
| **Recuperação** | Aguardar e tentar novamente |

### ERR-015: Timeout

| Propriedade | Valor |
|---|---|
| **Mensagem** | "A operação demorou mais que o esperado." |
| **Orientação** | "Tente novamente. Se o problema persistir, contate o suporte." |
| **Ação Sugerida** | Retry |
| **Impacto** | Médio |
| **Recuperação** | Retry ou contato suporte |

### ERR-016: Erro Interno

| Propriedade | Valor |
|---|---|
| **Mensagem** | "Ocorreu um erro inesperado." |
| **Orientação** | "Contate o suporte técnico com o código do erro: {codigo}" |
| **Ação Sugerida** | Contatar suporte |
| **Impacto** | Crítico |
| **Recuperação** | Contato com suporte técnico |

---

## 5. Erros de Permissão

### ERR-017: Acesso Negado

| Propriedade | Valor |
|---|---|
| **Mensagem** | "Você não tem permissão para esta ação." |
| **Orientação** | "Contate o administrador para solicitar acesso." |
| **Ação Sugerida** | Contatar administrador |
| **Impacto** | Médio |
| **Recuperação** | Solicitar permissão |

### ERR-018: Sessão Expirada

| Propriedade | Valor |
|---|---|
| **Mensagem** | "Sua sessão expirou." |
| **Orientação** | "Faça login novamente para continuar." |
| **Ação Sugerida** | Login |
| **Impacto** | Baixo |
| **Recuperação** | Re-login |

---

## 6. Mensagens de Sucesso

### MSG-001: Registro Criado

| Propriedade | Valor |
|---|---|
| **Mensagem** | "{entidade} criado(a) com sucesso." |
| **Tipo** | Sucesso |
| **Duração** | 5 segundos |

### MSG-002: Registro Atualizado

| Propriedade | Valor |
|---|---|
| **Mensagem** | "{entidade} atualizado(a) com sucesso." |
| **Tipo** | Sucesso |
| **Duração** | 5 segundos |

### MSG-003: Registro Excluído

| Propriedade | Valor |
|---|---|
| **Mensagem** | "{entidade} removido(a) com sucesso." |
| **Tipo** | Sucesso |
| **Duração** | 5 segundos |

### MSG-004: Ação Executada

| Propriedade | Valor |
|---|---|
| **Mensagem** | "{ação} realizada com sucesso." |
| **Tipo** | Sucesso |
| **Duração** | 5 segundos |

---

## Resumo de Erros

| Categoria | Quantidade |
|---|---|
| Validação | 4 |
| Estado | 4 |
| Negócio | 4 |
| Sistema | 4 |
| Permissão | 2 |
| Sucesso | 4 |
| **Total** | **22** |

---

## Validação

| Critério | Status |
|---|---|
| Todos os erros documentados | ✅ |
| Mensagens em português | ✅ |
| Sem mensagens técnicas | ✅ |
| Orientações claras | ✅ |
| Ações sugeridas | ✅ |
| Impacto classificado | ✅ |
| Recuperação definida | ✅ |
