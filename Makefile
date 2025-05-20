install:
	pip install -r requirements.txt

freeze:
	pip freeze > requirements.txt

run:
	uvicorn app.main:app --reload

migrate:
	alembic revision --autogenerate -m "Initial migration"

test:
	pytest -v

check:
	ruff check

format:
	ruff format
