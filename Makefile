

dev:
	uv run uvicorn main:app --reload


check:
	uv run mypy .


ci:
	uv run ruff check # linter
	uv run ruff format # formatter
	uv run mypy . # type checker
	uv run vulture src # dead code detector

docker-build:
	docker build -t auth-backend:latest .

docker-run:
	docker run -p 8000:8000 auth-backend:latest


#id 3 - AA1234 - ploves@gmail.com