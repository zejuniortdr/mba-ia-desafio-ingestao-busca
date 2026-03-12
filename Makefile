setup:
	python3 -m venv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements.txt


setup/dev:
	python3 -m venv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements-dev.txt


up:
	docker compose up -d


ingest:
	python3 src/ingest.py



chat:
	python3 src/chat.py


test:
	venv/bin/pytest tests/unit -v

test-integration:
	venv/bin/pytest tests/integration -v

test-all:
	venv/bin/pytest tests/ -v --tb=short
