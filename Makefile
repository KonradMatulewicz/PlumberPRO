.PHONY: install db migrate seed dev check test e2e perf
install:
	pip install -e ".[dev]"
db:
	docker compose up -d db
migrate:
	alembic upgrade head
seed:
	python -m app.simulator.seed --days 30 --seed 42
dev:
	uvicorn app.main:app --reload
check:
	ruff check app tests
	bandit -q -r app -lll
	pytest --cov --cov-report=term-missing
test:
	pytest
e2e:
	pytest -m e2e tests/e2e
perf:
	locust -f tests/perf/locustfile.py --headless -u 20 -r 5 -t 1m --host $${BASE_URL:-http://localhost:8000}
