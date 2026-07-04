#!/bin/bash
set -e

echo "=== Plantão 360 - Docker Compose Up ==="

docker compose up -d

echo ""
echo "=== Serviços rodando ==="
docker compose ps

echo ""
echo "=== Aguardando health check ==="
sleep 5

echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "Swagger: http://localhost:8000/api/v1/docs"
