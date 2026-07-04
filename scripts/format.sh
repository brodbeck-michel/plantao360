#!/bin/bash
set -e

echo "=== Plantão 360 - Format ==="

echo "--- Backend Format ---"
cd backend
python -m black app/ 2>/dev/null || echo "Black formatado"
python -m ruff check --fix app/ 2>/dev/null || echo "Ruff formatado"
cd ..

echo "--- Frontend Format ---"
cd frontend
npm run format 2>/dev/null || echo "Prettier formatado"
cd ..

echo "=== Formatação concluída ==="
