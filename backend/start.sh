#!/bin/sh
# Startup script for Plantão 360
#
# Responsabilidade deste script: garantir que o banco esteja acessível e então
# iniciar o uvicorn. As migrations, o seed (só DEMO) e a criação do admin são
# de responsabilidade do lifespan do app (app/core/lifespan.py + runtime.py),
# que roda antes de aceitar tráfego — fonte única, independente do launcher.
# (Antes, migrations/seed rodavam aqui E no lifespan: 2× no boot.)
set -e

ENVIRONMENT="${ENVIRONMENT:-development}"
PORT="${PORT:-8000}"
HOST="${HOST:-0.0.0.0}"

echo "[startup] Mode: $ENVIRONMENT"

# Step 0: Ensure data directory exists (legacy SQLite; harmless com Postgres)
mkdir -p /app/data
echo "[startup] Data directory ready: /app/data"

# Step 0.5: Wait for the database when using Postgres (avoids restart loop on boot)
case "${DATABASE_URL:-}" in
    postgresql*)
        echo "[startup] Waiting for database to be ready..."
        ATTEMPTS=0
        MAX_ATTEMPTS=30
        until python -c "import os; from sqlalchemy import create_engine, text; create_engine(os.environ['DATABASE_URL']).connect().execute(text('SELECT 1'))" 2>/dev/null; do
            ATTEMPTS=$((ATTEMPTS + 1))
            if [ "$ATTEMPTS" -ge "$MAX_ATTEMPTS" ]; then
                echo "[startup] ERROR: database not reachable after $MAX_ATTEMPTS attempts. Aborting."
                exit 1
            fi
            echo "[startup] Database not ready (attempt $ATTEMPTS/$MAX_ATTEMPTS). Retrying in 2s..."
            sleep 2
        done
        echo "[startup] Database is ready."
        ;;
esac

# Migrations + seed + admin: ver app/core/lifespan.py (rodam no startup do app,
# antes de servir tráfego). Não duplicar aqui.

# Uvicorn config
case "$ENVIRONMENT" in
    production)
        echo "[startup] Starting uvicorn in production mode (no reload)"
        exec uvicorn app.main:app --host "$HOST" --port "$PORT"
        ;;
    development|demo)
        echo "[startup] Starting uvicorn in development mode (with reload)"
        exec uvicorn app.main:app --host "$HOST" --port "$PORT" --reload
        ;;
    test)
        echo "[startup] Starting uvicorn in test mode"
        exec uvicorn app.main:app --host "$HOST" --port "$PORT"
        ;;
    *)
        echo "[startup] Unknown environment '$ENVIRONMENT', defaulting to development"
        exec uvicorn app.main:app --host "$HOST" --port "$PORT" --reload
        ;;
esac
