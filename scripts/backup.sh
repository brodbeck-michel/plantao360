#!/usr/bin/env bash
# ============================================================================
# Backup do banco PostgreSQL de produção do Plantão 360.
#
#   Uso:  ./scripts/backup.sh
#   Gera: backups/plantao360_AAAA-MM-DD_HHMMSS.sql
#
# Restauração (em banco limpo):
#   docker exec -i plantao360_db psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" < backups/<arquivo>.sql
#
# Recomendado agendar no cron do servidor, ex. (diário às 2h):
#   0 2 * * *  cd /apps/plantao360 && ./scripts/backup.sh >> /var/log/plantao360-backup.log 2>&1
# ============================================================================
set -euo pipefail

cd "$(dirname "$0")/.."

if [ ! -f .env.production ]; then
  echo "ERRO: .env.production não encontrado na raiz do projeto." >&2
  exit 1
fi

# Carrega POSTGRES_USER / POSTGRES_DB do .env.production
set -a
# shellcheck disable=SC1091
. ./.env.production
set +a

: "${POSTGRES_USER:?POSTGRES_USER não definido no .env.production}"
: "${POSTGRES_DB:?POSTGRES_DB não definido no .env.production}"

mkdir -p backups
STAMP="$(date +%Y-%m-%d_%H%M%S)"
OUT="backups/plantao360_${STAMP}.sql"

echo "==> Gerando backup do banco '${POSTGRES_DB}' em ${OUT} ..."
docker exec plantao360_db pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" > "$OUT"
echo "==> Backup concluído: ${OUT} ($(wc -c < "$OUT") bytes)"
