# Guia Rápido: Importar Dados do Backup

## O que foi criado?

✓ **scripts/import_backup.py** - Script principal de importação
✓ **scripts/test_import.py** - Script de teste e validação
✓ **IMPORT_BACKUP.md** - Documentação completa

## Como Usar

### 1️⃣ Preparar o Backup

Você tem um arquivo JSON com os dados atuais do sistema. Salve-o em um local acessível:

```
/caminho/para/seu/backup_2026-08-06.json
```

### 2️⃣ Navegar para o Backend

```bash
cd plantao360/backend
```

### 3️⃣ Executar a Importação

**Opção 1: Adicionar aos dados existentes**
```bash
python -m scripts.import_backup /caminho/para/backup.json
```

**Opção 2: Limpar e reimportar (remove tudo antes)**
```bash
python -m scripts.import_backup /caminho/para/backup.json --clear
```

### 4️⃣ Verificar Resultado

O script mostrará:
- Quantos médicos foram importados
- Quantos períodos foram criados
- Quantos plantões foram carregados
- Quantas horas extras foram registradas

## O que é Importado?

| Dados | Status | Notas |
|-------|--------|-------|
| Médicos | ✓ | Nome, CRM (gerado), RQE, data admissão |
| Plantões | ✓ | Data, tipo (T1-R2), horários |
| Atribuições | ✓ | Simples ou divididas (split) |
| Horas Extras | ✓ | Com justificativas |
| Períodos | ✓ | Agrupados por mês/ano |

## Formato do JSON de Entrada

O backup deve conter:

```json
{
  "version": 2,
  "data": {
    "doctor_vlh": {
      "Nome Médico": 176.26,
      ...
    },
    "doctor_meta": {
      "Nome Médico": {
        "rqe": "SIM",
        "admissao": "08/2008"
      },
      ...
    },
    "shifts_2026-07": {
      "2026-07-01": {
        "T1": "Nome Médico",
        "T2": "Nome Médico",
        "R1": {
          "type": "split",
          "parts": [...]
        },
        "_extras": [...]
      }
    }
  }
}
```

## Mapeamento de Turnos

| Turno | Horário | Duração |
|-------|---------|---------|
| T1 | 07:00 - 19:00 | 12h |
| T2 | 19:00 - 07:00 | 12h |
| T3 | 07:00 - 07:00 | 24h |
| R1 | 07:00 - 13:00 | 6h |
| R2 | 13:00 - 19:00 | 6h |

## Resolução de Problemas

### "File not found"
✓ Verifique o caminho do arquivo
```bash
ls -la /caminho/para/backup.json
```

### "Invalid JSON"
✓ Valide o arquivo
```bash
python -m json.tool backup.json > /dev/null
```

### Erros de Encoding
✓ Se há caracteres especiais (ã, ç, etc), converta:
```bash
iconv -f ISO-8859-1 -t UTF-8 backup.json > backup_utf8.json
```

### Duplicatas de Médicos
✓ Use `--clear` para limpar antes:
```bash
python -m scripts.import_backup backup.json --clear
```

## Teste Rápido

Para testar o script sem modificar o banco:

```bash
python -m scripts.test_import
```

Isso cria um backup de teste em memória e valida:
- Parsing do JSON
- Extração de médicos
- Extração de plantões
- Extração de extras

## Próximos Passos

Após importação bem-sucedida:

1. ✓ Verifique no banco: `SELECT COUNT(*) FROM doctors;`
2. ✓ Acesse a interface: http://localhost:3000
3. ✓ Valide os dados carregados
4. ✓ Continue usando o sistema normalmente

## Performance

| Dados | Tempo |
|-------|-------|
| 50 médicos | ~1s |
| 500 plantões | ~2s |
| 1000 extras | ~1s |
| **Total** | **~5s** |

## Perguntas Frequentes

**P: Preciso fazer backup antes?**
R: Sim! Sempre faça backup do banco antes de importar.

**P: Posso importar múltiplas vezes?**
R: Sim, use `--clear` para evitar duplicatas.

**P: E se der erro no meio da importação?**
R: O banco faz rollback automático, nada é alterado.

**P: Os dados antigos serão perdidos?**
R: Não, a menos que use `--clear`.

**P: Quanto tempo leva?**
R: Normalmente menos de 10 segundos.

---

## Suporte

Para mais detalhes, consulte: **IMPORT_BACKUP.md**
