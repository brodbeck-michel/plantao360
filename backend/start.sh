#!/bin/sh
# Startup script for Plantão 360
# Reads ENVIRONMENT env var and runs the appropriate initialization flow.
#
# Modes:
#   DEMO:       migrations → seed demo → start API
#   DEVELOPMENT: migrations → start API
#   PRODUCTION:  migrations → start API
#   TEST:        start API (no migrations, no seed)
set -e

ENVIRONMENT="${ENVIRONMENT:-development}"
RELOAD_FLAG=""
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

# Step 1: Database migrations (skip for test mode)
if [ "$ENVIRONMENT" != "test" ]; then
    echo "[startup] Running database migrations..."
    alembic upgrade head
    echo "[startup] Migrations completed successfully."
fi

# Step 2: Seed data (only in DEMO mode)
# NOTE: Seed failures must NOT prevent the server from starting.
if [ "$ENVIRONMENT" = "development" ]; then
    DEMO_MODE="${DEMO_MODE:-false}"
    if [ "$DEMO_MODE" = "true" ]; then
        echo "[startup] DEMO_MODE detected — seeding demo data..."
        if python -m app.seed.seed_data --dataset demo --clear; then
            echo "[startup] Seed completed successfully."
        else
            echo "[startup] WARNING: Seed failed (exit code $?). Server will start anyway."
        fi
    else
        echo "[startup] No seed — DEVELOPMENT mode without DEMO_MODE"
    fi
fi

# Step 3: Uvicorn config
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
