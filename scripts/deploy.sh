#!/usr/bin/env bash
# ============================================================================
# Deploy do Plantão 360 em produção a partir de imagens já publicadas no GHCR.
#
#   Uso:       edite APP_VERSION no .env da raiz, depois ./scripts/deploy.sh
#   Rollback:  troque APP_VERSION para a versão anterior e rode de novo
#
# NUNCA compila no servidor — apenas baixa (pull) e sobe (up -d). Equivalente a:
#   docker compose pull && docker compose up -d
#
# Pré-requisitos no servidor: docker + docker compose, um arquivo .env na raiz
# com COMPOSE_FILE=docker-compose.prod.yml e APP_VERSION=X.Y.Z, e um
# .env.production preenchido (a partir de .env.production.example).
# ============================================================================
set -euo pipefail

cd "$(dirname "$0")/.."

if [ ! -f .env ]; then
  echo "ERRO: .env não encontrado na raiz do projeto." >&2
  echo "      Crie com: COMPOSE_FILE=docker-compose.prod.yml e APP_VERSION=X.Y.Z" >&2
  exit 1
fi

if [ ! -f .env.production ]; then
  echo "ERRO: .env.production não encontrado na raiz do projeto." >&2
  echo "      Copie de .env.production.example e preencha os valores." >&2
  exit 1
fi

APP_VERSION="$(grep -E '^APP_VERSION=' .env | cut -d= -f2-)"
echo "==> Deploy Plantão 360 | APP_VERSION=${APP_VERSION:-<não definido em .env>}"

echo "==> Baixando imagens..."
if ! docker compose pull; then
  echo "ERRO: falha ao baixar as imagens da versão '${APP_VERSION}'." >&2
  echo "      Verifique: (1) a versão existe no GHCR; (2) se as imagens forem" >&2
  echo "      privadas, rode 'docker login ghcr.io' com um token read:packages." >&2
  exit 1
fi

echo "==> Subindo serviços (db -> backend -> frontend)..."
docker compose up -d

echo "==> Estado dos serviços:"
docker compose ps

echo "==> Deploy concluído (APP_VERSION=${APP_VERSION})."
echo "    Logs do backend:  docker compose logs -f backend"
