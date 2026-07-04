.PHONY: setup up down lint test format migrate revision downgrade shell logs clean seed help

help: ## Mostra esta ajuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Configura o projeto (copia .env, instala dependências)
	bash scripts/setup.sh

up: ## Sobe os containers
	docker compose up -d

down: ## Derruba os containers
	docker compose down

lint: ## Executa lint (ruff + black + eslint)
	bash scripts/lint.sh

test: ## Executa testes
	bash scripts/test.sh

format: ## Formata o código
	bash scripts/format.sh

migrate: ## Executa migrações (make migrate)
	cd backend && alembic upgrade head

revision: ## Cria nova migração (make revision MESSAGE="nome")
	cd backend && alembic revision --autogenerate -m "$(MESSAGE)"

downgrade: ## Desfaz última migração
	cd backend && alembic downgrade -1

shell: ## Abre shell Python no backend
	docker compose exec backend python -c "from app.core.config import get_settings; print(get_settings().dict())"

logs: ## Mostra logs dos containers
	docker compose logs -f

clean: ## Limpa caches, __pycache__, .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf backend/.coverage backend/htmlcov frontend/dist

seed: ## Carrega dados de demonstracao (make seed DATASET=demo)
	cd backend && python -m app.seed run $(or $(DATASET),demo) --clear
