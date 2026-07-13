#!/usr/bin/env bash
# ============================================================================
# Deploy do Plantão 360 em produção a partir de imagens já publicadas no GHCR.
#
#   Uso:       TAG=v1.2.0 ./scripts/deploy.sh
#   Rollback:  rode de novo com a TAG anterior, ex.:  TAG=v1.1.0 ./scripts/deploy.sh
#
# NUNCA compila no servidor — apenas baixa (pull) e sobe (up -d).
# Pré-requisitos no servidor: docker + docker compose, `docker login ghcr.io`,
# e um arquivo .env.production preenchido (a partir de .env.production.example).
# ============================================================================
set -euo pipefail

# Vai para a raiz do projeto (um nível acima de scripts/)
cd "$(dirname "$0")/.."

COMPOSE_FILE="docker-compose.prod.yml"
TAG="${TAG:-latest}"
export TAG

echo "==> Deploy Plantão 360 | TAG=${TAG}"

if [ ! -f .env.production ]; then
  echo "ERRO: .env.production não encontrado na raiz do projeto." >&2
  echo "      Copie de .env.production.example e preencha os valores." >&2
  exit 1
fi

echo "==> Baixando imagens da tag '${TAG}' no GHCR..."
docker compose -f "$COMPOSE_FILE" pull

echo "==> Subindo serviços (db -> backend -> frontend)..."
docker compose -f "$COMPOSE_FILE" up -d

echo "==> Estado dos serviços:"
docker compose -f "$COMPOSE_FILE" ps

echo "==> Deploy concluído (TAG=${TAG})."
echo "    Logs do backend:  docker compose -f ${COMPOSE_FILE} logs -f backend"
