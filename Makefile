# ==============================================================================
# Makefile — PDF Chat RAG
# ==============================================================================

.PHONY: setup setup/dev up check-env ingest chat test test-integration test-all lint fmt

# ------------------------------------------------------------------------------
# Setup
# ------------------------------------------------------------------------------

envvars:
	cp .env.example .env

env:
	python3 -m venv venv
	venv/bin/pip install --upgrade pip

setup: env envvars
	venv/bin/pip install -r requirements.txt


setup/dev: env envvars
	venv/bin/pip install -r requirements-dev.txt

# ------------------------------------------------------------------------------
# Infraestrutura
# ------------------------------------------------------------------------------

up:
	docker compose up -d

# ------------------------------------------------------------------------------
# Validação do .env
# ------------------------------------------------------------------------------

check-env:
	@echo "🔍 Verificando variáveis de ambiente..."
	@if [ ! -f .env.example ]; then \
		echo "❌ Arquivo .env.example não encontrado."; \
		exit 1; \
	fi
	@if [ ! -f .env ]; then \
		echo "❌ Arquivo .env não encontrado."; \
		echo "   Execute: cp .env.example .env  e preencha as variáveis."; \
		exit 1; \
	fi
	@MISSING=0; \
	while IFS= read -r line || [ -n "$$line" ]; do \
		line=$$(echo "$$line" | sed 's/#.*//;s/[[:space:]]*$$//'); \
		[ -z "$$line" ] && continue; \
		KEY=$$(echo "$$line" | cut -d= -f1); \
		[ -z "$$KEY" ] && continue; \
		VALUE=$$(grep -E "^$$KEY[[:space:]]*=" .env 2>/dev/null | cut -d= -f2- | sed 's/[[:space:]]*//'); \
		if [ -z "$$VALUE" ]; then \
			echo "  ❌ Variável não preenchida: $$KEY"; \
			MISSING=1; \
		else \
			echo "  ✅ $$KEY"; \
		fi; \
	done < .env.example; \
	if [ "$$MISSING" -eq 1 ]; then \
		echo ""; \
		echo "⚠️  Preencha todas as variáveis no arquivo .env antes de continuar."; \
		exit 1; \
	fi; \
	echo ""; \
	echo "✅ Todas as variáveis estão preenchidas!"

# ------------------------------------------------------------------------------
# Execução
# ------------------------------------------------------------------------------

ingest: check-env
	python3 src/ingest.py

chat: check-env
	python3 src/chat.py

# ------------------------------------------------------------------------------
# Testes
# ------------------------------------------------------------------------------

test:
	venv/bin/pytest tests/unit -v

test-integration:
	venv/bin/pytest tests/integration -v

test-all:
	venv/bin/pytest tests/ -v --tb=short

# ------------------------------------------------------------------------------
# Qualidade de Código
# ------------------------------------------------------------------------------

lint:
	venv/bin/ruff check src/ tests/

fmt:
	venv/bin/ruff format src/ tests/
