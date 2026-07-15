

dev:
	uv run uvicorn main:app --reload


check:
	uv run mypy .


ci:
	uv run ruff check # linter
	uv run ruff format # formatter
	uv run mypy . # type checker
	uv run vulture src # dead code detector
