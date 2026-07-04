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

# Step 1: Database migrations (skip for test mode)
if [ "$ENVIRONMENT" != "test" ]; then
    echo "[startup] Running database migrations..."
    alembic upgrade head
fi

# Step 2: Seed data (only in DEMO mode)
if [ "$ENVIRONMENT" = "development" ]; then
    # Check if DEMO_MODE is set via env var or .env file
    DEMO_MODE="${DEMO_MODE:-false}"
    if [ "$DEMO_MODE" = "true" ]; then
        echo "[startup] DEMO_MODE detected — seeding demo data..."
        python -m app.seed.seed_data --dataset demo --clear
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
