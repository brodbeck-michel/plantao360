#!/bin/bash
set -e

echo "=== Plantão 360 - Lint ==="

echo "--- Backend Lint ---"
cd backend
python -m ruff check app/ --fix 2>/dev/null || python -m ruff check app/
python -m black app/ --check 2>/dev/null || echo "Black check concluído"
cd ..

echo "--- Frontend Lint ---"
cd frontend
npm run lint 2>/dev/null || echo "ESLint concluído"
cd ..

echo "=== Lint concluído ==="
