# Script para setup do projeto

set -e

echo "=== Plantão 360 - Setup ==="

# Copiar .env se não existir
if [ ! -f .env ]; then
    echo "Criando .env a partir de .env.development..."
    cp .env.development .env
fi

# Backend setup
echo "--- Backend Setup ---"
cd backend
if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual..."
    python -m venv venv
fi

# Instalar pre-commit
echo "Instalando pre-commit..."
pip install pre-commit --quiet 2>/dev/null || true
pre-commit install 2>/dev/null || true

cd ..

# Frontend setup
echo "--- Frontend Setup ---"
cd frontend
if [ ! -d "node_modules" ]; then
    echo "Instalando dependências do frontend..."
    npm install
fi
cd ..

echo "=== Setup concluído ==="
echo ""
echo "Para subir o projeto:"
echo "  docker compose up -d"
echo ""
echo "Ou para desenvolvimento local:"
echo "  cd backend && source venv/bin/activate && uvicorn app.api.app:app --reload"
echo "  cd frontend && npm run dev"
