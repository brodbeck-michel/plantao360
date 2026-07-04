# Operational Workspace Review — Sprint 16

## ETAPA 0 — Auditoria do Fluxo Atual

---

## Como o coordenador trabalha hoje?

O coordenador utiliza uma planilha (Excel/Google Sheets) para montar a competência mensal do PS Unimed Tubarão. A planilha tem a seguinte estrutura:

### Estrutura da Planilha Atual

```
| DATA       | T1 TITULAR MANHÃ  | T2 TITULAR TARDE | T3 TITULAR NOITE | R1 REFORÇO MANHÃ | R2 REFORÇO TARDE |
|------------|--------------------|------------------|------------------|------------------|------------------|
| Sex 26/Jun | [dropdown médico] | [dropdown médico]| [dropdown médico]| [dropdown médico]| [dropdown médico]|
| Sáb 27/Jun | [dropdown médico] | [dropdown médico]| [dropdown médico]| [dropdown médico]| [dropdown médico]|
| ...        | ...                | ...              | ...              | ...              | ...              |
```

### Configuração dos Turnos

| Turno | Nome                  | Horário        | Carga Horária |
|-------|-----------------------|----------------|---------------|
| T1    | Titular Manhã         | 07:00–12:59    | 6h            |
| T2    | Titular Tarde         | 13:00–18:59    | 6h            |
| T3    | Titular Noite         | 19:00–06:59*   | 12h           |
| R1    | Reforço Manhã         | 09:00–14:59    | 6h            |
| R2    | Reforço Tarde         | 15:00–21:00    | 6h            |

### Funcionalidades da Planilha

- **Dropdowns** com lista de médicos em cada célula
- **Botão de expandir** (⊕) para cada linha do dia
- **Tabs**: Planilha | Resumo | Médicos | Turnos | Remuneração | Relatório por Período
- **Legenda**: Titular | Reforço | Dividido | Extra
- **Toolbar**: Botões de Salvar, CSV, Dados, Importar
- **Navegação temporal**: Ano + botões < >

---

## Quais ações são feitas dezenas de vezes por dia?

| Ação                              | Frequência     | Descrição |
|-----------------------------------|----------------|-----------|
| **Selecionar médico na célula**   | ~150-200x/mês  | O coordenador clica no dropdown e seleciona o médico para cada turno de cada dia |
| **Trocar médico**                 | ~50-80x/mês    | Quando um médico não pode, o coordenador troca por outro na mesma célula |
| **Copiar médico para outros dias**| ~30-50x/mês    | Quando o mesmo médico trabalha vários dias seguidos |
| **Visualizar cobertura**          | ~20-30x/mês    | Verificar quantos turnos estão preenchidos vs total |
| **Identificar conflitos**         | ~10-20x/mês    | Verificar se um médico já está escalado em outro turno no mesmo dia |
| **Adicionar extra**               | ~5-10x/mês     | Registrar horas extras de um médico |
| **Salvar**                        | ~10-20x/mês    | Salvar o estado da planilha |
| **Exportar**                      | ~2-5x/mês      | Gerar CSV para envio |

---

## Quantos cliques existem?

### Ação: Montar um dia completo (5 turnos)

| Passo | Ação                          | Cliques |
|-------|-------------------------------|---------|
| 1     | Clicar no dropdown T1         | 1       |
| 2     | Selecionar médico             | 1       |
| 3     | Clicar no dropdown T2         | 1       |
| 4     | Selecionar médico             | 1       |
| 5     | Clicar no dropdown T3         | 1       |
| 6     | Selecionar médico             | 1       |
| 7     | Clicar no dropdown R1         | 1       |
| 8     | Selecionar médico             | 1       |
| 9     | Clicar no dropdown R2         | 1       |
| 10    | Selecionar médico             | 1       |
| **Total** | **10 cliques por dia**    | **10**  |

### Ação: Montar competência inteira (30 dias)

- **30 dias × 10 cliques = 300 cliques** apenas para selecionar médicos
- **+ ~50 cliques** para correções e trocas
- **+ ~20 cliques** para salvar e navegar
- **Total: ~370 cliques** para montar uma competência

### Ação: Trocar médico em 1 turno

| Passo | Ação                          | Cliques |
|-------|-------------------------------|---------|
| 1     | Clicar no dropdown            | 1       |
| 2     | Selecionar novo médico        | 1       |
| **Total** | **2 cliques**             | **2**   |

---

## Onde existem gargalos?

### Gargalo 1: Troca de competência
- O coordenador precisa navegar para outro mês e recarregar tudo
- A planilha não mantém contexto ao trocar de mês

### Gargalo 2: Visualização de conflitos
- O coordenador precisa **olhar manualmente** se um médico já está escalado em outro turno no mesmo dia
- Não há indicador visual automático de conflito

### Gargalo 3: Cobertura
- O coordenador precisa **contar manualmente** quantos turnos estão preenchidos
- A aba "Resumo" mostra isso, mas requer troca de aba

### Gargalo 4: Carga horária por médico
- O coordenador precisa ir na aba "Médicos" para ver quantas horas cada médico já tem
- Não há visão integrada na grade

### Gargalo 5: Extras
- Extras são registrados separadamente
- Não aparecem integrados na grade

### Gargalo 6: Validação
- Não há validação automática de:
  - Limite de horas por médico
  - Especialidade compatível com o turno
  - Conflito de horário (mesmo médico em dois turnos sobrepostos)

---

## O que deve permanecer?

| Elemento                        | Por quê |
|---------------------------------|---------|
| **Grade diária (DATA × TURNOS)**| Estrutura intuitiva e comprovada |
| **Dropdowns de médico**         | Rápido e familiar |
| **Visão mensal**                | Perspectiva completa da competência |
| **Tabs (Resumo, Médicos, etc.)**| Organização lógica |
| **Legenda de cores**            | Comunicação visual rápida |
| **Navegação temporal (< >)**    | Troca rápida de competência |
| **Toolbar com ações**           | Acesso rápido a operações |

---

## O que deve desaparecer?

| Elemento                          | Por quê |
|-----------------------------------|---------|
| **Planilha como ferramenta**      | Não tem validação, não tem rastreabilidade |
| **Contagem manual de conflitos**  | Deve ser automática |
| **Troca de aba para ver resumo**  | Resumo deve estar integrado |
| **Contagem manual de cobertura**  | Deve ser calculada em tempo real |
| **Exportação manual**             | Deve ser automática |
| **Falta de undo**                 | Deve ter desfazer |

---

## Fluxo Atual

```
Planilha Excel/Sheets
  ↓
Abrir arquivo
  ↓
Navegar para mês correto
  ↓
Preencher célula por célula (dropdown)
  ↓
Verificar conflitos manualmente
  ↓
Verificar cobertura em outra aba
  ↓
Salvar localmente
  ↓
Exportar CSV para envio
  ↓
Copiar dados para sistema legado (se aplicável)
```

## Fluxo Plantão 360

```
Plantão 360 — Operational Workspace
  ↓
Abrir competência (1 clique)
  ↓
Grade visual com todos os dias × turnos
  ↓
Clicar na célula → QuickAssign (1 clique)
  ↓
Conflitos detectados automaticamente (cores)
  ↓
Cobertura calculada em tempo real (sidebar)
  ↓
Salvar (1 clique, com undo)
  ↓
Exportar CSV (1 clique)
  ↓
Dados já no sistema (sem cópia manual)
```

## Ganhos Operacionais

| Métrica                        | Atual (Planilha) | Plantão 360 | Ganho |
|--------------------------------|-------------------|-------------|-------|
| **Cliques por competência**    | ~370              | ~60-80      | **~80% redução** |
| **Tempo para montar**          | 2-4 horas         | 30-60 min   | **~65% redução** |
| **Detecção de conflitos**      | Manual            | Automática  | **100% automação** |
| **Cálculo de cobertura**       | Manual            | Tempo real  | **100% automação** |
| **Rastreabilidade**            | Nenhuma           | Completa    | **De 0 para 100%** |
| **Validação de regras**        | Nenhuma           | Automática  | **De 0 para 100%** |
| **Undo**                       | Ctrl+Z manual     | Integrado   | **Melhor UX** |
| **Colaboração**                | Arquivo único     | Multi-usuário| **Novo** |
| **Backup/Versão**              | Manual            | Automático  | **Novo** |

---

## Referência: Sistema Atual (Imagem)

A imagem mostra a planilha atual com:
- Header verde escuro com nome "PS Unimed Tubarão"
- Toolbar com botões: Salvar, CSV, Dados, Importar
- Navegação: ANO 2026 + botões < >
- Período: 26/Jun/2026 – 25/Jul/2026
- Tabs: Planilha, Resumo, Médicos, Turnos, Remuneração, Relatório por Período
- Legenda: Titular, Reforço, Dividido, Extra
- Grade com DATA × TURNOS (T1, T2, T3, R1, R2)
- Dropdowns em cada célula
- Botão ⊕ para expandir dia
- Indicador "6 turnos preenchidos"

**Preservar**: organização da grade, velocidade operacional, baixa quantidade de cliques, visão mensal, facilidade para trocar médicos.

**Não copiar**: aparência, código, layout antigo, limitações, tecnologia.
