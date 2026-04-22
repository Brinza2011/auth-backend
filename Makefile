

dev:
	uv run uvicorn main:app --reload


check:
	uv run mypy .
