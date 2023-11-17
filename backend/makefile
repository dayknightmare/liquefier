.PHONY: test
test:
	python -m pytest --cov src --cov-report=html tests/ -v -x --cache-clear
	@coverage json -o htmlcov/coverage.json

	$(eval percent := $(shell python config/coverage_checker.py htmlcov/coverage.json))

	@echo "Units => $(percent)%"

.PHONY: make-migrations
make-migrations:
	alembic revision --autogenerate

.PHONY: make-migration-manually
make-migration-manually:
	alembic revision

.PHONY: migrate
migrate:
	alembic upgrade head

.PHONY: run
run:
	gunicorn \
		--preload \
		--workers=8 \
		--bind=0.0.0.0:8000 \
		--worker-class uvicorn.workers.UvicornWorker \
		--worker-connections 4096 \
		main:app \
		--max-requests-jitter=10 \
		--max-requests=100
