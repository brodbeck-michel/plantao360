# Importar Dados do Backup

Script para importar dados da versão anterior do sistema de plantões para o novo sistema Plantao360.

## Uso

### Pré-requisitos

- Python 3.12+
- Banco de dados PostgreSQL/SQLite inicializado
- Arquivo de backup em formato JSON

### Executar Importação

```bash
# Simples (mantém dados existentes)
python -m scripts.import_backup /caminho/para/backup.json

# Limpar banco e importar
python -m scripts.import_backup /caminho/para/backup.json --clear
```

### Exemplos

```bash
# Importar backup local
cd backend
python -m scripts.import_backup ../data/backup_2026-08-06.json

# Importar e limpar banco anterior
python -m scripts.import_backup ../data/backup_2026-08-06.json --clear
```

## Estrutura de Dados Mapeada

### Médicos
- `doctor_vlh` → Doctor (horas totais)
- `doctor_meta` → Doctor metadata (RQE, data admissão)

### Plantões
- `shifts_YYYY-MM` → Periods, Shifts, ShiftParts

### Turnos
- T1: 07:00-19:00 (12h)
- T2: 19:00-07:00 (12h)
- T3: 07:00-07:00 (24h)
- R1: 07:00-13:00 (6h)
- R2: 13:00-19:00 (6h)

### Horas Extras
- `_extras` → ShiftExtra (com justificativa)

## Validações

O script realiza as seguintes validações:

1. ✓ Carrega arquivo JSON do backup
2. ✓ Cria/atualiza médicos (evita duplicatas por CRM)
3. ✓ Cria períodos (ano/mês)
4. ✓ Cria plantões com horários
5. ✓ Atribui médicos aos plantões (simples ou split)
6. ✓ Importa horas extras com justificativas
7. ✓ Suporta --clear para limpar banco antes

## O que é Importado

### Dados Importados
- ✓ Médicos e metadados
- ✓ Períodos (meses/anos)
- ✓ Plantões agendados
- ✓ Atribuições de médicos (com horas)
- ✓ Horas extras justificadas
- ✓ Status dos plantões (completed)

### Dados NÃO Importados
- ✗ Usuários do sistema (use seed com --dataset admin)
- ✗ Auditorias anteriores
- ✗ Histórico de alterações

## Troubleshooting

### "File not found"
Certifique-se que o caminho para o backup está correto:
```bash
ls -la /caminho/para/backup.json
```

### "Invalid JSON"
Valide o arquivo JSON:
```bash
python -m json.tool backup.json > /dev/null
```

### Erros de Encoding
Se há erros com caracteres especiais (ã, ç, etc):
```bash
# Converter encoding se necessário
iconv -f ISO-8859-1 -t UTF-8 backup.json > backup_utf8.json
```

### Duplicatas de CRM
O script cria CRM baseado em hash do nome do médico. Se houver conflito:
1. Edite manualmente os nomes dos médicos no JSON, ou
2. Use `--clear` para limpar e reimportar

## Performance

- ~50 médicos: ~1s
- ~500 plantões: ~2s
- ~1000 extras: ~1s

Total esperado para backup completo: **~5s**

## Suporte

Para problemas:
1. Verifique logs: `python -m scripts.import_backup backup.json 2>&1 | tee import.log`
2. Valide JSON: `python -m json.tool backup.json`
3. Confirme schema do banco: `python -c "from app.models import *; print('OK')"`
