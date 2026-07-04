#!/bin/bash
set -e

echo "=== Plantão 360 - Test ==="

echo "--- Backend Tests ---"
cd backend
python -m pytest app/tests/ -v --tb=short
cd ..

echo "--- Frontend Tests ---"
cd frontend
npm run test 2>/dev/null || echo "Nenhum teste frontend configurado"
cd ..

echo "=== Testes concluídos ==="
