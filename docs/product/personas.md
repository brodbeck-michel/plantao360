# Personas — Plantão 360

**Sprint:** 11 — Product Design, User Experience Modeling & Frontend Functional Specification
**Data:** 2026-06-27

---

## 1. Coordenador Médico

### Identidade
- **Nome:** Dr. Carlos Eduardo Silva
- **Idade:** 45 anos
- **Formação:** Médico, Especialista em Gestão Hospitalar
- **Cargo:** Coordenador de Escalas Médicas

### Responsabilidades
- Montar e distribuir escalas de plantão mensalmente
- Atribuir médicos a plantões
- Resolver conflitos de agenda
- Aprovar coberturas
- Monitorar cobertura da instituição
- Reportar indicadores ao Diretor

### Objetivos
- Garantir 100% de cobertura dos plantões
- Minimizar conflitos de agenda
- Reduzir horas extras desnecessárias
- Manter equilíbrio na distribuição de plantões

### Dores
- Dificuldade em visualizar conflitos de agenda em tempo real
- Processo manual de distribuição de plantões consome muito tempo
- Falta de visibilidade sobre disponibilidade de médicos
- Dificuldade em prever demanda futura

### Frequência de Uso
- **Diária:** 2-4 horas
- **Pico:** Início do mês (montagem de escala)

### Dispositivos Utilizados
- Desktop (80%)
- Tablet (15%)
- Celular (5%)

### Nível Técnico
- Médio
- Usa sistemas hospitalares há 10+ anos
- Não programa

### Indicadores Acompanhados
- % de cobertura de plantões
- Número de conflitos de agenda
- Horas extras por médico
- Tempo médio de resolução de conflitos

### Permissões
- CRUD de Médicos
- CRUD de Períodos
- CRUD de Plantões
- CRUD de Atribuições
- Aprovar/Rejeitar Coberturas
- Consultar Analytics
- Consultar KPIs

### Operações Críticas
1. Montar escala mensal
2. Atribuir médico a plantão
3. Resolver conflito de cobertura
4. Aprovar cobertura

---

## 2. Médico Plantonista

### Identidade
- **Nome:** Dra. Ana Maria Santos
- **Idade:** 38 anos
- **Formação:** Médica, Clínica Geral
- **Cargo:** Médica Plantonista

### Responsabilidades
- Realizar plantões escalados
- Solicitar coberturas quando necessário
- Registrar extras de plantão
- Consultar sua agenda
- Confirmar atribuições

### Objetivos
- Ter visibilidade clara da sua agenda
- Facilmente solicitar cobertura
- Receber notificações importantes
- Consultar sua remuneração

### Dores
- Dificuldade em ver sua agenda completa
- Processo demorado para solicitar cobertura
- Falta de transparência na remuneração
- Notificações atrasadas

### Frequência de Uso
- **Semanal:** 1-2 horas
- **Pico:** Antes do plantão

### Dispositivos Utilizados
- Celular (60%)
- Desktop (30%)
- Tablet (10%)

### Nível Técnico
- Básico
- Usa smartphone para tudo
- Prefere apps simples

### Indicadores Acompanhados
- Próximos plantões
- Horas trabalhadas no mês
- Remuneração prevista
- Coberturas pendentes

### Permissões
- Consultar Médicos (próprio)
- Consultar Períodos
- Consultar Plantões (próprios)
- Consultar Atribuições (próprias)
- Solicitar Cobertura
- Consultar Extras (próprios)
- Consultar Payroll (próprio)

### Operações Críticas
1. Consultar agenda
2. Solicitar cobertura
3. Confirmar atribuição
4. Consultar remuneração

---

## 3. Financeiro

### Identidade
- **Nome:** Roberto Fernando Costa
- **Idade:** 42 anos
- **Formação:** Contador, Pós-graduação em Finanças Hospitalares
- **Cargo:** Gerente Financeiro

### Responsabilidades
- Consolidar dados financeiros dos períodos
- Validar remunerações
- Aprovar processamento de folha
- Gerar relatórios financeiros
- Monitorar KPIs financeiros

### Objetivos
- Garantir precisão dos dados financeiros
- Cumprir prazos de folha
- Reduzir inconsistências financeiras
- Ter visibilidade em tempo real

### Dores
- Dificuldade em consolidar dados de múltiplas fontes
- Processo manual de validação consome tempo
- Falta de rastreabilidade de cálculos
- Dificuldade em explicar valores para médicos

### Frequência de Uso
- **Diária:** 3-4 horas
- **Pico:** Fechamento de competência

### Dispositivos Utilizados
- Desktop (90%)
- Tablet (10%)

### Nível Técnico
- Médio-Alto
- Usa Excel avançado
- Entende de dados

### Indicadores Acompanhados
- Total de remuneração por período
- Número de inconsistências
- Tempo de processamento de folha
- % de dados validados

### Permissões
- Consultar Todos os Dados
- Aprovar Payroll
- Processar Payroll
- Consultar Analytics
- Consultar KPIs Financeiros

### Operações Críticas
1. Consolidar dados financeiros
2. Validar remuneração
3. Aprovar processamento
4. Gerar relatório

---

## 4. RH (Recursos Humanos)

### Identidade
- **Nome:** Mariana Oliveira Lima
- **Idade:** 35 anos
- **Formação:** Administradora, Pós-graduação em RH
- **Cargo:** Analista de RH Hospitalar

### Responsabilidades
- Cadastrar e atualizar dados de médicos
- Gerenciar vínculos empregatícios
- Validar CRM e especialidades
- Monitorar carga horária
- Gerar relatórios de pessoal

### Objetivos
- Manter dados de médicos atualizados
- Garantir conformidade de vínculos
- Otimizar processo de cadastro
- Ter visibilidade sobre carga horária

### Dores
- Cadastro manual consome tempo
- Dificuldade em validar dados de CRM
- Falta de integração com sistemas de RH
- Dificuldade em acompanhar carga horária

### Frequência de Uso
- **Semanal:** 2-3 horas
- **Pico:** Admissão de novos médicos

### Dispositivos Utilizados
- Desktop (85%)
- Tablet (15%)

### Nível Técnico
- Médio
- Usa sistemas de RH
- Não programa

### Indicadores Acompanhados
- Número de médicos ativos
- Carga horária por médico
- CRM validados
- Novos cadastros

### Permissões
- CRUD de Médicos
- Consultar Períodos
- Consultar Plantões
- Consultar Atribuições

### Operações Críticas
1. Cadastrar novo médico
2. Atualizar dados
3. Validar CRM
4. Consultar carga horária

---

## 5. Auditor

### Identidade
- **Nome:** José Pedro Ferreira
- **Idade:** 50 anos
- **Formação:** Engenheiro, Auditor Interno
- **Cargo:** Auditor de Processos

### Responsabilidades
- Auditar processos de folha de pagamento
- Verificar conformidade de aprovações
- Rastrear decisões e mudanças
- Gerar relatórios de auditoria
- Identificar irregularidades

### Objetivos
- Garantir rastreabilidade total
- Verificar conformidade de processos
- Identificar fraudes e erros
- Gerar evidências de auditoria

### Dores
- Dificuldade em rastrear decisões
- Falta de transparência em processos
- Processo manual de auditoria consome tempo
- Dificuldade em explicar achados

### Frequência de Uso
- **Mensal:** 8-16 horas
- **Pico:** Fechamento de competência

### Dispositivos Utilizados
- Desktop (95%)
- Tablet (5%)

### Nível Técnico
- Alto
- Usa ferramentas de auditoria
- Entende de dados e processos

### Indicadores Acompanhados
- Número de auditorias realizadas
- Achados de conformidade
- Tempo de resposta
- % de processos auditados

### Permissões
- Consultar Todos os Dados
- Consultar Analytics
- Consultar KPIs
- Consultar Timeline
- Consultar Audit Trail

### Operações Críticas
1. Consultar histórico de mudanças
2. Verificar aprovações
3. Rastrear decisões
4. Gerar relatório de auditoria

---

## 6. Administrador

### Identidade
- **Nome:** Fernanda Souza Martins
- **Idade:** 40 anos
- **Formação:** Ciência da Computação, Pós-graduação em Gestão de TI
- **Cargo:** Administrador do Sistema

### Responsabilidades
- Gerenciar permissões de usuários
- Configurar parâmetros do sistema
- Monitorar performance
- Resolver problemas técnicos
- Gerenciar integrações

### Objetivos
- Garantir disponibilidade do sistema
- Manter segurança dos dados
- Otimizar performance
- Facilitar uso pelos usuários

### Dores
- Dificuldade em monitorar performance
- Falta de dashboards de monitoramento
- Processo manual de configuração
- Dificuldade em diagnosticar problemas

### Frequência de Uso
- **Diária:** 1-2 horas
- **Pico:** Quando há problemas

### Dispositivos Utilizados
- Desktop (90%)
- Celular (10%)

### Nível Técnico
- Alto
- Programa
- Entende de infraestrutura

### Indicadores Acompanhados
- Uptime do sistema
- Tempo de resposta
- Número de erros
- Uso de recursos

### Permissões
- Acesso Total
- Gerenciar Usuários
- Configurar Sistema
- Consultar Logs
- Gerenciar Integrações

### Operações Críticas
1. Monitorar sistema
2. Configurar parâmetros
3. Gerenciar permissões
4. Resolver problemas

---

## 7. Diretor Hospitalar

### Identidade
- **Nome:** Dr. Paulo Henrique Almeida
- **Idade:** 55 anos
- **Formação:** Médico, MBA em Gestão Hospitalar
- **Cargo:** Diretor Administrativo

### Responsabilidades
- Tomar decisões estratégicas
- Aprovar políticas e processos
- Monitorar indicadores de alto nível
- Aprovar orçamentos
- Reportar ao conselho

### Objetivos
- Ter visão consolidada da operação
- Tomar decisões baseadas em dados
- Garantir eficiência operacional
- Maximizar retorno financeiro

### Dores
- Falta de visão consolidada
- Dificuldade em acessar dados relevantes
- Processos lentos de aprovação
- Falta de indicadores estratégicos

### Frequência de Uso
- **Semanal:** 1-2 horas
- **Pico:** Reuniões de diretoria

### Dispositivos Utilizados
- Tablet (50%)
- Desktop (30%)
- Celular (20%)

### Nível Técnico
- Básico
- Usa tablet para relatórios
- Não programa

### Indicadores Acompanhados
- KPIs estratégicos
- Resultados financeiros
- Satisfação de médicos
- Eficiência operacional

### Permissões
- Consultar Analytics
- Consultar KPIs
- Consultar Relatórios
- Aprovar Payroll (alto nível)

### Operações Críticas
1. Consultar dashboard estratégico
2. Aprovar processamento de folha
3. Revisar indicadores
4. Gerar relatório para conselho

---

## Resumo das Personas

| Persona | Frequência | Dispositivo Principal | Nível Técnico |
|---|---|---|---|
| Coordenador Médico | Diária | Desktop | Médio |
| Médico Plantonista | Semanal | Celular | Básico |
| Financeiro | Diária | Desktop | Médio-Alto |
| RH | Semanal | Desktop | Médio |
| Auditor | Mensal | Desktop | Alto |
| Administrador | Diária | Desktop | Alto |
| Diretor | Semanal | Tablet | Básico |

---

## Validação

| Critério | Status |
|---|---|
| Todas as personas documentadas | ✅ |
| Responsabilidades definidas | ✅ |
| Objetivos definidos | ✅ |
| Dores documentadas | ✅ |
| Frequência de uso definida | ✅ |
| Dispositivos mapeados | ✅ |
| Nível técnico definido | ✅ |
| Indicadores listados | ✅ |
| Permissões mapeadas | ✅ |
| Operações críticas listadas | ✅ |
